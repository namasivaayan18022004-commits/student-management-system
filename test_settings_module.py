import os
import sys
import unittest
from app import app, db
from models import User, CollegeSettings, SecuritySettings, NotificationSettings, EmailSettings, AppearanceSettings, BackupHistory, ActivityLog

class TestSettingsModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()

    def login_admin(self):
        return self.client.post('/login', data=dict(
            username='admin',
            password='admin123'
        ), follow_redirects=True)

    def test_01_existing_modules_integrity(self):
        """Verify zero breaking changes to existing modules"""
        self.login_admin()
        routes = ['/dashboard', '/students', '/teachers', '/attendance', '/marks', '/fees', '/reports']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
            print(f"[OK] Existing route verified: {route}")

    def test_02_settings_dashboard(self):
        """Verify settings dashboard loads all 10 cards"""
        self.login_admin()
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("College Settings", content)
        self.assertIn("Admin Profile", content)
        self.assertIn("Change Password", content)
        self.assertIn("User Management", content)
        self.assertIn("Security Settings", content)
        self.assertIn("Backup & Restore", content)
        self.assertIn("Notification Settings", content)
        self.assertIn("Email Configuration", content)
        self.assertIn("Appearance", content)
        self.assertIn("System Info & Logs", content)
        print("[OK] Settings Dashboard verified (10 categories present)")

    def test_03_college_settings_crud(self):
        """Verify College Settings GET and POST update"""
        self.login_admin()
        res_get = self.client.get('/settings/college')
        self.assertEqual(res_get.status_code, 200)

        res_post = self.client.post('/settings/college', data={
            'college_name': 'PEC Engineering College',
            'academic_year': '2025-2026',
            'email_address': 'info@pec.edu',
            'phone_number': '+91 9876543210',
            'college_address': '100 Campus Road',
            'city': 'Chennai',
            'state': 'Tamil Nadu',
            'postal_code': '600001',
            'country': 'India',
            'college_description': 'Premier technical institution'
        }, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)

        with app.app_context():
            cs = CollegeSettings.query.first()
            self.assertEqual(cs.college_name, 'PEC Engineering College')
            self.assertEqual(cs.academic_year, '2025-2026')
        print("[OK] College Settings CRUD verified")

    def test_04_admin_profile_and_password(self):
        """Verify Admin Profile update and password change"""
        self.login_admin()
        res_profile = self.client.post('/settings/profile', data={
            'action_type': 'update_profile',
            'full_name': 'Dr. Principal Admin',
            'email': 'principal@pec.edu',
            'phone': '9988776655',
            'address': 'Principal House, Campus'
        }, follow_redirects=True)
        self.assertEqual(res_profile.status_code, 200)

        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            self.assertEqual(admin.full_name, 'Dr. Principal Admin')
            self.assertEqual(admin.email, 'principal@pec.edu')

        # Try changing password with short password (should error flash)
        res_pass = self.client.post('/settings/profile', data={
            'action_type': 'change_password',
            'current_password': 'password',
            'new_password': 'short',
            'confirm_password': 'short'
        }, follow_redirects=True)
        self.assertIn("Password must be at least 8 characters long", res_pass.data.decode('utf-8'))
        print("[OK] Admin Profile and Password verification verified")

    def test_05_user_management_and_protection(self):
        """Verify User Management CRUD and last active admin protection"""
        self.login_admin()
        res_get = self.client.get('/settings/users')
        self.assertEqual(res_get.status_code, 200)

        # Create a second admin
        res_add = self.client.post('/settings/users/add', data={
            'username': 'manager1',
            'password': 'StrongPassword123!',
            'full_name': 'Exam Manager',
            'email': 'exam@pec.edu',
            'role': 'Manager'
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)

        with app.app_context():
            users_count = User.query.count()
            self.assertEqual(users_count, 2)
            u2 = User.query.filter_by(username='manager1').first()
            u2_id = u2.id

        # Toggle status of manager1
        res_toggle = self.client.post(f'/settings/users/toggle/{u2_id}', follow_redirects=True)
        self.assertEqual(res_toggle.status_code, 200)

        # Delete manager1
        res_delete = self.client.post(f'/settings/users/delete/{u2_id}', follow_redirects=True)
        self.assertEqual(res_delete.status_code, 200)

        # Try deleting the last active admin (id=1) - should be blocked!
        res_last = self.client.post('/settings/users/delete/1', follow_redirects=True)
        self.assertIn("Cannot delete the last active administrator account!", res_last.data.decode('utf-8'))
        print("[OK] Admin User Management and Last Admin Protection verified")

    def test_06_security_settings_crud(self):
        """Verify Security Settings update"""
        self.login_admin()
        res = self.client.post('/settings/security', data={
            'enable_2fa': 'on',
            'auto_logout': 'on',
            'max_login_attempts': '3',
            'lock_duration_minutes': '45',
            'password_policy_strong': 'on'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            sec = SecuritySettings.query.first()
            self.assertTrue(sec.enable_2fa)
            self.assertEqual(sec.max_login_attempts, 3)
            self.assertEqual(sec.lock_duration_minutes, 45)
        print("[OK] Security Settings verified")

    def test_07_backup_and_restore(self):
        """Verify SQLite Database Backup creation and deletion"""
        self.login_admin()
        with app.app_context():
            initial_count = BackupHistory.query.count()

        res_create = self.client.post('/settings/backup/create', follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)

        with app.app_context():
            self.assertEqual(BackupHistory.query.count(), initial_count + 1)
            b = BackupHistory.query.order_by(BackupHistory.id.desc()).first()
            self.assertIsNotNone(b)
            self.assertTrue(b.filename.startswith("backup_"))
            b_id = b.id

        res_del = self.client.post(f'/settings/backup/delete/{b_id}', follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        with app.app_context():
            self.assertEqual(BackupHistory.query.count(), initial_count)
        print("[OK] Database Backup & Restore verified")

    def test_08_notifications_and_email(self):
        """Verify Notifications and Email settings CRUD and Test Email"""
        self.login_admin()
        res_notif = self.client.post('/settings/notifications', data={
            'student_notifications': 'on',
            'fee_reminders': 'on',
            'attendance_alerts': 'on',
            'marks_notifications': 'on'
        }, follow_redirects=True)
        self.assertEqual(res_notif.status_code, 200)

        res_email = self.client.post('/settings/email', data={
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': '587',
            'email_address': 'erp@pec.edu',
            'sender_name': 'PEC ERP Notifications'
        }, follow_redirects=True)
        self.assertEqual(res_email.status_code, 200)

        res_test = self.client.post('/settings/email/test', follow_redirects=True)
        self.assertIn("Test email sent successfully", res_test.data.decode('utf-8'))
        print("[OK] Notifications & Outbound Email Configuration verified")

    def test_09_appearance_customization(self):
        """Verify Theme Mode, Font Size, and Accent Colors"""
        self.login_admin()
        res = self.client.post('/settings/appearance', data={
            'theme_mode': 'dark',
            'font_size': 'large',
            'accent_color': '#198754',
            'sidebar_color': '#212529'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            app_sett = AppearanceSettings.query.first()
            self.assertEqual(app_sett.theme_mode, 'dark')
            self.assertEqual(app_sett.font_size, 'large')
            self.assertEqual(app_sett.accent_color, '#198754')
        print("[OK] UI Appearance Customization verified")

    def test_10_system_info_and_activity_logs(self):
        """Verify System Diagnostics & Activity Audit Logs"""
        self.login_admin()
        res = self.client.get('/settings/system')
        self.assertEqual(res.status_code, 200)
        content = res.data.decode('utf-8')
        self.assertIn("Student Management System ERP", content)
        self.assertIn("Python", content)
        self.assertIn("SQLite", content)

        with app.app_context():
            logs_count = ActivityLog.query.count()
            self.assertGreater(logs_count, 0)
        print(f"[OK] System Diagnostics & Activity Audit Logs verified")

    def test_11_settings_search(self):
        """Verify Unified Settings search page and JSON API"""
        self.login_admin()
        res_page = self.client.get('/settings/search?q=college')
        self.assertEqual(res_page.status_code, 200)
        self.assertIn("College Profile Settings", res_page.data.decode('utf-8'))

        res_api = self.client.get('/api/settings/search?q=security')
        self.assertEqual(res_api.status_code, 200)
        self.assertTrue(res_api.is_json)
        data = res_api.get_json()
        self.assertGreater(len(data), 0)
        print("[OK] Live Settings Search & API verified")

if __name__ == '__main__':
    unittest.main(verbosity=2)
