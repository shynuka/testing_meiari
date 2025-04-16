from django.test import SimpleTestCase
from django.urls import reverse, resolve
from meiari_v1.views import (AppCheckAPIView, DownloadReportAPIView, GeminiReportResponse, MeiAriUserCreateAPIView,
                          ReportBySubDeptOfficeAPIView, SignInAPIView, OTPVerifyAPIView, TNGovtDeptAPIView,
                          TNGovtDeptContactAPIView, TNGovtSubDeptAPIView, SubDeptDetailsAPIView,
                          SubDeptOfficeDetailsAPIView, UpdateTicketStatusAPIView, WorkGroupAPIView,
                          WorkGroupDetailAPIView, WorkGroupListBySubDeptAPIView, WorkGroupMembersAPIView,
                          WorkGroupMembersListAPIView, WorkGroupTicketAPIView, WorkGroupTicketStatusCountAPIView,
                          CreateWorkGroupWithDetailsAPIView, GenerateAndUploadReport)

import uuid


class TestUrls(SimpleTestCase):

    def test_app_check_url_resolves(self):
        url = reverse('geminiapp-check')
        self.assertEquals(resolve(url).func.view_class, AppCheckAPIView)

    def test_create_meiari_user_url_resolves(self):
        url = reverse('create-meiari-user')
        self.assertEquals(resolve(url).func.view_class, MeiAriUserCreateAPIView)

    def test_verify_otp_url_resolves(self):
        url = reverse('verify-otp')
        self.assertEquals(resolve(url).func.view_class, OTPVerifyAPIView)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEquals(resolve(url).func.view_class, SignInAPIView)

    def test_tngovt_dept_url_resolves(self):
        url = reverse('tngovtdept')
        self.assertEquals(resolve(url).func.view_class, TNGovtDeptAPIView)

    def test_tngovt_dept_contact_url_resolves(self):
        url = reverse('tngovtdept-contact')
        self.assertEquals(resolve(url).func.view_class, TNGovtDeptContactAPIView)

    def test_tngovt_sub_dept_url_resolves(self):
        url = reverse('tngovtsubdept')
        self.assertEquals(resolve(url).func.view_class, TNGovtSubDeptAPIView)

    def test_subdept_details_url_resolves(self):
        url = reverse('subdeptdetails')
        self.assertEquals(resolve(url).func.view_class, SubDeptDetailsAPIView)

    def test_subdept_office_details_url_resolves(self):
        url = reverse('subdeptofficedetails')
        self.assertEquals(resolve(url).func.view_class, SubDeptOfficeDetailsAPIView)

    def test_workgroup_url_resolves(self):
        url = reverse('workgroup')
        self.assertEquals(resolve(url).func.view_class, WorkGroupAPIView)

    def test_workgroup_details_url_resolves(self):
        url = reverse('workgroup-detail')
        self.assertEquals(resolve(url).func.view_class, WorkGroupDetailAPIView)

    def test_workgroup_members_url_resolves(self):
        url = reverse('workgroup-members')
        self.assertEquals(resolve(url).func.view_class, WorkGroupMembersAPIView)

    def test_workgroup_members_list_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('workgroup-members', kwargs={'work_group_id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, WorkGroupMembersListAPIView)

    def test_workgroup_ticket_url_resolves(self):
        url = reverse('workgroup-ticket')
        self.assertEquals(resolve(url).func.view_class, WorkGroupTicketAPIView)

    def test_get_workgroup_ticket_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('get-workgroup-ticket', kwargs={'ticket_id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, WorkGroupTicketAPIView)

    def test_ticket_status_count_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('ticket-status-count', kwargs={'work_group_id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, WorkGroupTicketStatusCountAPIView)

    def test_create_workgroup_with_details_url_resolves(self):
        url = reverse('create-workgroup-with-details')
        self.assertEquals(resolve(url).func.view_class, CreateWorkGroupWithDetailsAPIView)

    def test_workgroup_list_by_subdept_url_resolves(self):
        url = reverse('workgroup-list-by-subdept')
        self.assertEquals(resolve(url).func.view_class, WorkGroupListBySubDeptAPIView)

    def test_generate_and_upload_report_url_resolves(self):
        url = reverse('generate-and-upload-report')
        self.assertEquals(resolve(url).func.view_class, GenerateAndUploadReport)

    def test_gemini_report_response_url_resolves(self):
        url = reverse('gemini-report-response')
        self.assertEquals(resolve(url).func.view_class, GeminiReportResponse)

    def test_report_by_sub_dept_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('report-by-sub-dept', kwargs={'sub_dept_office_id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, ReportBySubDeptOfficeAPIView)

    def test_update_ticket_status_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('update-ticket-status', kwargs={'id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, UpdateTicketStatusAPIView)

    def test_download_report_url_resolves(self):
        test_uuid = uuid.uuid4()
        url = reverse('download-report', kwargs={'id': test_uuid})
        self.assertEquals(resolve(url).func.view_class, DownloadReportAPIView)
