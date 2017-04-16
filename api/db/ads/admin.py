# from sqlalchemy import create_engine, MetaData,Index
# from sqlalchemy import Table, Column, Integer, String, JSON, Boolean, DateTime, ForeignKey, \
#     ForeignKeyConstraint, Sequence
# from sqlalchemy.schema import UniqueConstraint
# from sqlalchemy.dialects.postgresql.json import JSONB
# from sqlalchemy.orm import sessionmaker, scoped_session, relationship, mapper, relation,aliased
# from sqlalchemy.ext.declarative import declarative_base
#
# import os
# import datetime
# import pytz
# from utils.funcs import reshape_orm_result
# import logging
# from dictalchemy import DictableModel
# from dictalchemy.utils import make_class_dictable
#
# # logging.basicConfig(level=logging.DEBUG)
# # logging.getLogger('sqlalchemy.engine.base').setLevel(logging.DEBUG)
#
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{id}:{pw}@/{db}'.format(id='YasumasaTakemura', pw='yasu0708',
#                                                                          db='postgres')
# # SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
#
#
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
# metadata = MetaData()
# metadata.bind = engine
# Session = sessionmaker(autoflush=False, bind=engine)
# DBSession = scoped_session(sessionmaker())
# session = Session()
# conn = engine.connect()
#
# Base = declarative_base(cls=DictableModel)
# Base = make_class_dictable(Base)
#
# USER_ID = Sequence('user_id_seq', start=1)
# ACCOUNT_ID = Sequence('account_id_seq', start=1)
# TODOLIST_ID = Sequence('todolist_id_seq', start=1)
# REQUEST_ID = Sequence('myrequest_id_seq', start=1)
#
# timezone = 'Asia/Tokyo'
# now = datetime.datetime.now(pytz.timezone(timezone))
#
#
# def find_username(id):
#     try:
#         name = session.query(User.username).filter(User.user_id == id).first()
#         return name[0]
#     except:
#         return False
#
#
# def find_id(username):
#     try:
#         return session.query(User.user_id, Account.account_id, ToDoList.todo_id).filter_by(username=username).all()
#
#     except:
#         return False
#
#
# def find_user_id(username):
#     try:
#         my_id = session.query(User.user_id).filter_by(username=username).first()
#         return my_id[0]
#     except:
#         return False
#
#
# def find_group_id(user_id):
#     try:
#         group = session.query(Group.group_id).filter(Group.member_id == user_id).all()
#         return group
#     except Exception as e:
#         return False
#
#
# def find_account(username):
#     try:
#         id = session.query(Account.account_id).filter_by(username=username).all()
#         return id
#     except:
#         return False
#
#
# def account_register(login_user, account):
#     # Get user_id
#     user_id = find_user_id(login_user)
#
#     # Get account_id and name
#     registered_accounts = find_account(login_user)
#
#     # Create new account
#     if registered_accounts == False:
#
#         session.add(Account(user_id=user_id, account=account))
#         session.commit()
#         return session.query(Account.account_id).filter_by(account=account).first()[0]
#
#     # Get existed account_id
#     else:
#         return session.query(Account.account_id).filter_by(account=account).first()[0]
#
#
# class User(Base):
#     __tablename__ = 'manager_user'
#
#     user_id = Column(Integer, USER_ID, autoincrement=True, primary_key=True,)
#     username = Column(String, unique=True, nullable=True)
#     password = Column(String, nullable=False)
#     public = Column(Boolean, default=True, nullable=False)
#     description = Column(String, nullable=True)
#     icon = Column(String, nullable=True)
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('Account')
#     relationship('ToDoList')
#     relationship('Group')
#     relationship('CommentForTasks')
#     relationship('TaskListUserSetting')
#
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.username
#
# class Account(Base):
#     __tablename__ = 'manager_account'
#     __table_args__ = tuple(UniqueConstraint('user_id', 'account', name='user_id_account'))
#
#     user_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     account_id = Column(Integer, autoincrement=True, primary_key=True)
#
#     accountName = Column(String, nullable=False, unique=True)
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('Account')
#     relationship('ToDoList')
#     # relationship('Requests')
#
#
# class ToDoList(Base):
#     __tablename__ = 'manager_todolist'
#     extend_existing = True
#
#     todo_id = Column(Integer, autoincrement=True, primary_key=True)
#     user_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     account_id = Column(Integer, ForeignKey('manager_account.account_id'), nullable=False)
#
#     createdBy = Column(String, nullable=True)
#     title = Column(String, nullable=False)
#     requestTo = Column(String, nullable=False, default=user_id)
#     requestFrom = Column(String, nullable=True)
#
#     form = Column(String, nullable=False)
#     attachment = Column(String, nullable=False)
#     schedule = Column(DateTime, nullable=False)
#     taskStatus = Column(String,
#                         default='onRequest')  # nothing, on_request, accepted, declined ,doing , completed , retry,
#     completed = Column(Boolean, default=False)
#     comment = Column(String, nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('Account')
#
#
# class TaskList(Base):
#     __tablename__ = 'TaskList'
#     extend_existing = True
#
#     todoID = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'))
#     # accountID = Column(Integer, ForeignKey('manager_account.account_id'))
#
#     title = Column(String, nullable=False)
#     requestTo = Column(String)
#     requestFrom = Column(String, nullable=True)
#
#     formID = Column(Integer, ForeignKey('manager_form_template.form_id'), nullable=True)
#     attachment = Column(String, nullable=True)
#     schedule = Column(DateTime, nullable=True)
#     # [nothing, on_request, accepted, declined ,ongoing , completed , retry]
#     taskStatus = Column(String, default='self', nullable=True)
#     completed = Column(Boolean, default=False)
#     comment = Column(String, nullable=True)
#     committed = Column(Boolean, default=False,nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('CommentForTasks')
#
#
# class CommentForTasks(Base):
#     __tablename__ = 'CommentForTasks'
#     extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'),nullable=False)
#     todoID = Column(Integer, ForeignKey('TaskList.todoID'),nullable=False)
#     username = Column(String, nullable=False, default=find_username(userID))
#     comments = Column(String, nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
#
# class ScheduleForTasks(Base):
#     __tablename__ = 'ScheduleForTasks'
#     extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'),nullable=False)
#     todoID = Column(Integer, ForeignKey('TaskList.todoID'),nullable=False)
#     username = Column(String, nullable=False)
#     start = Column(DateTime, nullable=False)
#     end = Column(DateTime, nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
# class AttachmentForTasks(Base):
#     __tablename__ = 'AttachmentForTasks'
#     extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'),nullable=False)
#     todoID = Column(Integer, ForeignKey('TaskList.todoID'),nullable=False)
#     username = Column(String, nullable=False)
#     attachment = Column(String, nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
# class FormsForTasks(Base):
#     __tablename__ = 'FormsForTasks'
#     extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'),nullable=False)
#     todoID = Column(Integer, ForeignKey('TaskList.todoID'),nullable=False)
#     username = Column(String, nullable=False)
#     forms = Column(JSON, nullable=False)
#
#     createdAt = Column(DateTime, default=now)
#     updatedAt = Column(DateTime, default=now, onupdate=now)
#
#
#
# class TaskListUserSetting(Base):
#     __tablename__ = 'TaskListUserSetting'
#     extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     userID = Column(Integer, ForeignKey('manager_user.user_id'))
#     setting = Column(JSON, nullable=False)
#     user = relation('User', backref='TaskListUserSetting', foreign_keys=[userID])
#
#
# # __table_args__ = (UniqueConstraint('group_title', 'manager_id', name='UQ_group_title_manager_id'),)
#
# class Friend(Base):
#     __tablename__ = 'friend'
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     my_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     friend_id = Column(Integer,ForeignKey('manager_user.user_id'),nullable=False)
#     status = Column(String, nullable=False, default='inviting')
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     user = relation('User', backref='friend',foreign_keys=[my_id])
#     friend = relation('User', backref='_friend',foreign_keys=[friend_id])
#
# ###################
# ## Group management
# ###################
#
# class Group(Base):
#     __tablename__ = 'manager_group'
#     extend_existing = True
#
#     # extend_existing = True
#
#     group_id = Column(Integer, autoincrement=True, primary_key=True)
#     group_title = Column(String, nullable=False)
#     manager_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     icon = Column(String, nullable=True)
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('GroupManager')
#
#
#
# class GroupManager(Base):
#     __tablename__ = 'GroupManager'
#     extend_existing = True
#
#     # extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     group_id = Column(Integer, ForeignKey('manager_group.group_id'), nullable=False)
#     member_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=True)
#     status = Column(String, nullable=True, default='inviting')
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     group = relation('Group', backref='GroupManager',foreign_keys=[group_id])
#     relationship('User')
#
#
#
# class Addon(Base):
#     __tablename__ = 'Addon'
#     extend_existing = True
#
#     # extend_existing = True
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     manager_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     group_id = Column(Integer, ForeignKey('manager_group.group_id'), nullable=True)
#     addon_name = Column(String, nullable=True)  # table name
#     api_name = Column(String, nullable=False)
#     addon_id = Column(Integer, nullable=True)  # id in each table of contetnts
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('Group')
#     # relationship('Account')
#     # relationship('ToDoList')
#     # relationship('Requests')
#
#
# # template of forms which user has created
# class FormTemplate(Base):
#     __tablename__ = 'manager_form_template'
#     __table_args__ = tuple(UniqueConstraint('manager_id', 'form_title', name='manager_id_form_title'))
#     extend_existing = True
#
#     form_id = Column(Integer, autoincrement=True, primary_key=True)
#     manager_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     group_id = Column(Integer, ForeignKey('manager_group.group_id'), nullable=True)
#     form_title = Column(String, nullable=False, unique=True)
#     template = Column(JSON, nullable=False)
#     private = Column(Boolean, nullable=False, default=True)
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('Group')
#     relationship('TaskList')
#
#
# # this table will send to worker only
# class TaskManger(Base):
#     __tablename__ = 'taskManager'
#
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     manager_id = Column(Integer, ForeignKey('manager_user.user_id'), nullable=False)
#     title = Column(String, nullable=False)
#     tasks = Column(JSON, nullable=False)
#     start = Column(DateTime, nullable=True)
#     end = Column(DateTime, nullable=True)
#     schedule = Column(DateTime, nullable=False)
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('Group')
#
#
# # forms which users has filled in
# class FilledInForms(Base):
#     __tablename__ = 'FilledInForms'
#     ID = Column(Integer, primary_key=True)
#     formID = Column(Integer, ForeignKey('manager_form_template.form_id'), primary_key=True)
#     groupID = Column(Integer, ForeignKey('manager_group.group_id'), nullable=False)
#     filledInForm = Column(JSON, nullable=False)
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#     relationship('User')
#     relationship('Group')
#
#
# class InputType(Base):
#     __tablename__ = 'input_type'
#     #   __table_args__ = tuple(UniqueConstraint('user_id', 'account', name='user_id_account'))
#     #   extend_existing = True
#
#     inputId = Column(Integer, autoincrement=True, primary_key=True)
#     inputType = Column(String, nullable=False, )
#
#     created_at = Column(DateTime, default=now)
#     updated_at = Column(DateTime, default=now, onupdate=now)
#
#
# # class CampaignReport(Base):
# #     __tablename__ = 'campaign_report'
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     date = Column(String, nullable=False)
# #     company_name = Column(String, nullable=False)
# #     service_name = Column(String, nullable=True)
# #     campaign_name = Column(String, nullable=True)
# #     adset_name = Column(String, nullable=True,default='untitled')
# #     media = Column(String, nullable=False)
# #     spend = Column(Integer, nullable=True,default=0)
# #     impressions = Column(Integer, nullable=True,default=0)
# #     clicks = Column(Integer, nullable=True,default=0)
# #     cvs = Column(Integer, nullable=True,default=0)
# #     account_id = Column(Integer, nullable=True)
# #     campaign_id = Column(String, nullable=True)
# #     adset_id = Column(String, nullable=True)
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #     __table_args__ = (UniqueConstraint('date','campaign_id', 'adset_id',name='date_company_id_account_id_media'),)
# #
# # class AdjustEvents(Base):
# #     __tablename__ = 'adjust_events'
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     date = Column(DateTime, nullable=False)
# #     account_id = Column(Integer, ForeignKey('ad_account.id'),nullable=False)
# #     service_id = Column(Integer, ForeignKey('ad_services.id'), nullable=False)
# #     media_id = Column(Integer, ForeignKey('ad_media.id'), nullable=False)
# #     event_name =  Column(String, nullable=False)
# #     event_value =  Column(Integer, nullable=False)
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #
# #     relation('AdMedia')
# #     relation('AdAccount')
# #     relation('AdServices')
# #
# #     __table_args__ = (UniqueConstraint('date','account_id','service_id','media_id',name='unique_adjust'),)
# #
# #
# # class AdMedia(Base):
# #     __tablename__ = 'ad_media'
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     media_name = Column(String, nullable=False,unique=True)
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #
# #
# # class AdServices(Base):
# #     __tablename__ = 'ad_services'
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     service_name = Column(String, nullable=False,unique=False)
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #
# #
# # class AdAccount(Base):
# #     __tablename__ = 'ad_account'
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     account_name = Column(String, nullable=False)
# #
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #
# #     # __table_args__ = (UniqueConstraint('account_name','media_name',name='account_name_media_name'),)
# #     # relation('AdMedia')
# #
# #
# # class AdManager(Base):
# #     id = Column(Integer, autoincrement=True, primary_key=True)
# #     account_id = Column(Integer, ForeignKey('ad_account.id'),nullable=False)
# #     service_id = Column(Integer, ForeignKey('ad_services.id'), nullable=False)
# #     media_id = Column(Integer, ForeignKey('ad_media.id'), nullable=False)
# #     media_acccount_id = Column(String, ForeignKey('ad_services.id'), nullable=False)
# #     annual_budget = Column(Integer,nullable=True ,default=0 )
# #     monthly_budget = Column(Integer,nullable=True ,default=0 )
# #     daily_budget = Column(Integer,nullable=True ,default=0 )
# #
# #     reporting = Column(Boolean, nullable=False, default=True)
# #
# #     created_at = Column(DateTime, default=now)
# #     updated_at = Column(DateTime, default=now, onupdate=now)
# #
# #     relation('AdMedia')
# #     relation('AdAccount')
# #     relation('AdServices')
# #
#
# Base.metadata.create_all(bind=engine)
