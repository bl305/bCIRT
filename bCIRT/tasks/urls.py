from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views

app_name = 'tasks'

urlpatterns = [
    url(r'^get-file-zipped/(?P<ev_pk>\d+)/$', views.GetFileZippedView.as_view(), name='get_file_zipped'),
    url(r'^get-file-raw/(?P<ev_pk>\d+)/$', views.GetFileRawView.as_view(), name='get_file_raw'),

    url(r"^actions/$", views.ActionListView.as_view(), name="act_list"),
    url(r"^actions/new/$", views.ActionCreateView.as_view(), name="act_create"),
    url(r"^actions/detail/(?P<pk>\d+)/$", views.ActionDetailView.as_view(), name="act_detail"),
    url(r'^actions/edit/(?P<pk>\d+)/$', views.ActionUpdateView.as_view(), name='act_edit'),
    url(r'^actions/remove/(?P<pk>\d+)/$', views.ActionRemoveView.as_view(), name='act_remove'),

    url(r"^actions/qdetail/(?P<pk>\d+)/$", views.ActionQDetailView.as_view(), name="actq_detail"),
    url(r"^actions/exec/(?P<pk>\d+)/(?P<inv_pk>\d+)/(?P<task_pk>\d+)/(?P<ev_pk>\d+)/$",
        views.ActionExecScriptRedirectView.as_view(), name="act_exec_script"),

    url(r"^evidences/$", views.EvidenceListView.as_view(), name="ev_list"),
    url(r"^evidences/new/(?P<inv_pk>\d+)/(?P<task_pk>\d+)/$", views.EvidenceCreateView.as_view(), name="ev_create"),
    url(r"^evidences/detail/(?P<pk>\d+)/$", views.EvidenceDetailView.as_view(), name="ev_detail"),
    # url(r'^(?P<pk>\d+)/(?P<inv_pk>\d+)/(?P<task_pk>\d+)/edit/$', views.EvidenceUpdateView.as_view(), name='ev_edit'),
    url(r'^evidences/edit/(?P<pk>\d+)/$', views.EvidenceUpdateView.as_view(), name='ev_edit'),
    url(r'^evidences/remove/(?P<pk>\d+)/$', views.EvidenceRemoveView.as_view(), name='ev_remove'),

    url(r"^evidences/evattr$", views.EvidenceAttrListView.as_view(), name="evattr_list"),
    url(r"^evidences/evattr/new/(?P<pk>\d+)/$", views.EvidenceAttrCreateView.as_view(), name="evattr_create"),
    url(r"^evidences/evattr/detail/(?P<pk>\d+)/$", views.EvidenceAttrDetailView.as_view(), name="evattr_detail"),
    # url(r'^(?P<pk>\d+)/(?P<inv_pk>\d+)/(?P<task_pk>\d+)/edit/$', views.EvidenceUpdateView.as_view(), name='ev_edit'),
    url(r'^evidences/evattr/edit/(?P<pk>\d+)/$', views.EvidenceAttrUpdateView.as_view(), name='evattr_edit'),
    url(r'^evidences/evattr/remove/(?P<pk>\d+)/$', views.EvidenceAttrRemoveView.as_view(), name='evattr_remove'),

    url(r"^$", views.TaskListView.as_view(), name="tsk_list"),
    url(r"^new/(?P<inv_pk>\d+)/$", views.TaskCreateView.as_view(), name="tsk_create"),
    url(r"^detail/(?P<pk>\d+)/$", views.TaskDetailView.as_view(), name="tsk_detail"),
    url(r'^edit/(?P<pk>\d+)/$', views.TaskUpdateView.as_view(), name='tsk_edit'),
    url(r'^remove/(?P<pk>\d+)/$', views.TaskRemoveView.as_view(), name='tsk_remove'),
    url(r'^open/(?P<pk>\d+)/$', views.TaskOpenView.as_view(), name='tsk_open'),
    url(r'^assign/(?P<pk>\d+)/$', views.TaskAssignView.as_view(), name='tsk_assign'),
    url(r'^close/(?P<pk>\d+)/$', views.TaskCloseView.as_view(), name='tsk_close'),

    url(r"^tmp$", views.TaskTemplateListView.as_view(), name="tmp_list"),
    url(r"^tmp/new/$", views.TaskTemplateCreateView.as_view(), name="tmp_create"),
    url(r"^tmp/detail/(?P<pk>\d+)/$", views.TaskTemplateDetailView.as_view(), name="tmp_detail"),
    url(r'^tmp/edit/(?P<pk>\d+)/$', views.TaskTemplateUpdateView.as_view(), name='tmp_edit'),
    url(r'^tmp/remove/(?P<pk>\d+)/$', views.TaskTemplateRemoveView.as_view(), name='tmp_remove'),
    url(r"^tmp/add/(?P<pk>\d+)/(?P<inv_pk>\d+)/(?P<play_pk>\d+)/$", views.TaskTemplateAddView.as_view(),
        name="tmp_add"),

    url(r"^tvar$", views.TaskVarListView.as_view(), name="tvar_list"),
    url(r"^tvar/new/(?P<task_pk>\d+)/(?P<tasktmp_pk>\d+)/$", views.TaskVarCreateView.as_view(), name="tvar_create"),
    url(r"^tvar/detail/(?P<pk>\d+)/$", views.TaskVarDetailView.as_view(), name="tvar_detail"),
    url(r'^tvar/edit/(?P<pk>\d+)/$', views.TaskVarUpdateView.as_view(), name='tvar_edit'),
    url(r'^tvar/remove/(?P<pk>\d+)/$', views.TaskVarRemoveView.as_view(), name='tvar_remove'),

    url(r"^pb/$", views.PlaybookListView.as_view(), name="play_list"),
    url(r"^pb/new/(?P<tmp_pk>\d+)/(?P<inv_pk>\d+)/$", views.PlaybookCreateView.as_view(), name="play_create"),
    url(r"^pb/detail/(?P<pk>\d+)/$", views.PlaybookDetailView.as_view(), name="play_detail"),
    url(r'^pb/edit/(?P<pk>\d+)/$', views.PlaybookUpdateView.as_view(), name='play_edit'),
    url(r'^pb/remove/(?P<pk>\d+)/$', views.PlaybookRemoveView.as_view(), name='play_remove'),

    url(r"^pbtmp/$", views.PlaybookTemplateListView.as_view(), name="playtmp_list"),
    url(r"^pbtmp/new/$", views.PlaybookTemplateCreateView.as_view(), name="playtmp_create"),
    url(r"^pbtmp/detail/(?P<pk>\d+)/$", views.PlaybookTemplateDetailView.as_view(), name="playtmp_detail"),
    url(r'^pbtmp/edit/(?P<pk>\d+)/$', views.PlaybookTemplateUpdateView.as_view(), name='playtmp_edit'),
    url(r'^pbtmp/remove/(?P<pk>\d+)/$', views.PlaybookTemplateRemoveView.as_view(), name='playtmp_remove'),
    url(r"^pbtmp/export/(?P<pk>\d+)/$", views.PlaybookTemplateExportView.as_view(), name="playtmp_export"),

    url(r"^pbtmp/item$", views.PlaybookTemplateItemListView.as_view(), name="playittmp_list"),
    url(r"^pbtmp/item/new/(?P<play_pk>\d+)/$", views.PlaybookTemplateItemCreateView.as_view(), name="playittmp_create"),
    url(r"^pbtmp/item/detail/(?P<pk>\d+)/$", views.PlaybookTemplateItemDetailView.as_view(), name="playittmp_detail"),
    url(r'^pbtmp/item/edit/(?P<pk>\d+)/$', views.PlaybookTemplateItemUpdateView.as_view(), name='playittmp_edit'),
    url(r'^pbtmp/item/remove/(?P<pk>\d+)/$', views.PlaybookTemplateItemRemoveView.as_view(), name='playittmp_remove'),

    # url(r'^taskev/pdf/(?P<pk>\d+)', views.MyPDFView.as_view(), name='tskev_pdf'),


]
