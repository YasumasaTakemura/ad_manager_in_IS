from  time import time

from report.Ads.Dashboard.dashboard import Dashboard
from report.Ads.Facebook.Reports import CampaignReport as FBCampaignReport
from report.Ads.Manager.worker import fb_campagin_report_worker, im_campagin_report_worker, \
    tw_campagin_report_worker,nend_campagin_report_worker
from report.Ads.Nend.report import CampaignReport as NendCampaignReport
from report.Ads.Twitter.report import CampaignReport as TWCampaignReport
from report.Ads.imobile.report import CampaignReport as IMCampaignReport
from report.ads.Manager.ads_db_manager import Manager

Dashboard.get_daily_report_by_promotion()

im, tw, fb ,nend = Manager.queue_all_tasks()

print()

if __name__ == '__main__':

    start_time = time()

    for _fb in fb:
          fb_campagin_report_worker(FBCampaignReport,_fb)

    for _im in im:
          im_campagin_report_worker(IMCampaignReport,_im)

    for _tw in tw:
           tw_campagin_report_worker(TWCampaignReport,_tw)

    for _nend in nend:
         nend_campagin_report_worker(NendCampaignReport,_nend)


    finish_time = time()

    print(finish_time - start_time)
