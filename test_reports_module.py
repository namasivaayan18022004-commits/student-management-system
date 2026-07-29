import sys
import unittest
from app import app, db, User, Student, Teacher, Attendance, Mark, Fee, ReportHistory, ReportTemplate

class ReportsModuleTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def test_01_existing_modules_untouched(self):
        """Verify all existing modules load cleanly without errors"""
        # Login as admin
        response = self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        endpoints = [
            '/dashboard',
            '/students',
            '/teachers',
            '/attendance',
            '/marks',
            '/fees'
        ]
        for ep in endpoints:
            res = self.client.get(ep)
            self.assertEqual(res.status_code, 200, f"Failed to load existing endpoint {ep}: status {res.status_code}")
            print(f"[OK] Existing module endpoint {ep} -> Status {res.status_code}")

    def test_02_reports_pages(self):
        """Verify all Reports Module pages render with HTTP 200"""
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        
        pages = [
            '/reports',
            '/reports/categories',
            '/reports/generator',
            '/reports/view?category=student&report_type=Student+List',
            '/reports/view?category=teacher&report_type=Teacher+List',
            '/reports/view?category=attendance&report_type=Daily+Attendance',
            '/reports/view?category=marks&report_type=Rank+List',
            '/reports/view?category=fees&report_type=Fee+Collection+Report',
            '/reports/history',
            '/reports/scheduled',
            '/reports/search'
        ]
        for p in pages:
            res = self.client.get(p)
            self.assertEqual(res.status_code, 200, f"Failed to load report page {p}: status {res.status_code}")
            print(f"[OK] Report page {p} -> Status {res.status_code}")

    def test_03_instant_search_api(self):
        """Verify instant search API returns JSON results"""
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        res = self.client.get('/api/reports/search?q=a')
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertIsInstance(json_data, list)
        print(f"[OK] /api/reports/search -> Found {len(json_data)} records")

    def test_04_exports(self):
        """Verify CSV, Excel, and PDF export endpoints work without error"""
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        
        # Test CSV
        res_csv = self.client.get('/reports/export/csv?category=student&report_type=Student+List')
        self.assertEqual(res_csv.status_code, 200)
        self.assertEqual(res_csv.mimetype, 'text/csv')
        self.assertGreater(len(res_csv.data), 0)
        print("[OK] CSV Export generated successfully")

        # Test Excel
        res_excel = self.client.get('/reports/export/excel?category=student&report_type=Student+List')
        self.assertEqual(res_excel.status_code, 200)
        self.assertIn('spreadsheetml', res_excel.mimetype)
        self.assertGreater(len(res_excel.data), 0)
        print("[OK] Excel Export generated successfully")

        # Test PDF (HTML Print Preview view)
        res_pdf = self.client.get('/reports/export/pdf?category=student&report_type=Student+List')
        self.assertEqual(res_pdf.status_code, 200)
        self.assertIn(b'COLLEGE ERP SYSTEM', res_pdf.data)
        print("[OK] PDF/Print view generated successfully")

    def test_05_schedule_and_history(self):
        """Verify saving a template and checking history"""
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        
        res = self.client.post('/reports/scheduled/save', data={
            'template_name': 'Automated Test Template',
            'category': 'student',
            'report_type': 'Student List',
            'date_range': 'all'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Automated Test Template', res.data)
        print("[OK] Report template saved and listed successfully")

if __name__ == '__main__':
    unittest.main()
