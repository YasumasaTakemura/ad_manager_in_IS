from utils.funcs import validate_login, get_addon_by_groups, reshape_orm_result, today, yesterday
from db.ads import ads
from flask_cors import CORS, cross_origin
from flask import request, jsonify, Blueprint
from report.ads.Dashboard.dashboard import Dashboard
from report.ads.Facebook.Reports import CampaignReport as FBCampaignReport
from report.ads.Manager.worker import fb_campagin_report_worker, im_campagin_report_worker, \
    tw_campagin_report_worker, nend_campagin_report_worker
from report.ads.Nend.report import CampaignReport as NendCampaignReport
from report.ads.Twitter.report import CampaignReport as TWCampaignReport
from report.ads.imobile.report import CampaignReport as IMCampaignReport
from report.ads.Manager.ads_db_manager import Manager

# bind db connection
session = ads.session

###########################
# BluePrint
###########################
# crate blueprint instance
app = Blueprint('ads', __name__)

###########################
# CORS
###########################
CORS(app, resources={r"/*": {"origins": "*"}})


###########################
# export_excel
###########################
@app.route('/api/v1/export_excel', methods=['GET', 'POST'])
def export_excel():
    if request.method == 'GET':

        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        if start_time is None or end_time is None:
            start_time = yesterday().strftime('%Y-%m-%d')
            end_time = today().strftime('%Y-%m-%d')

        im, tw, fb, nend = Manager.queue_all_tasks()

        print(fb)
        for _fb in fb:
            fb_campagin_report_worker(FBCampaignReport, _fb, start_time, end_time)

        for _im in im:
            im_campagin_report_worker(IMCampaignReport, _im, start_time)

        for _nend in nend:
            nend_campagin_report_worker(NendCampaignReport, _nend, start_time)

        # for _tw in tw:
        #      tw_campagin_report_worker(TWCampaignReport, _tw)

        header, kpis = Dashboard.get_daily_report_by_promotion(start_time, end_time)
        data = {"header": header, "data": kpis}
        return jsonify(data=data)

    return jsonify(data='done!!')