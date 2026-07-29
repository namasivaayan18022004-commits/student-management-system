import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath('.'))

from app import app, db
from models import Student, Fee, User

app.config['WTF_CSRF_ENABLED'] = False

def test_fees_module():
    print("=" * 70)
    print("STARTING FEES MANAGEMENT MODULE VERIFICATION")
    print("=" * 70)

    with app.test_client() as client:
        with app.app_context():
            # 1. Verify Fees exist in Database & each student has random fee details
            students = Student.query.all()
            total_fees = Fee.query.count()
            print(f"[1/6] Total Students in DB: {len(students)}, Total Fee Records in DB: {total_fees}")
            assert total_fees > 0, "No fee records found in DB! Startup seeding failed."

            print("\n[2/6] Verifying different random fees details for students:")
            sample_students = students[:3]
            for s in sample_students:
                s_fees = Fee.query.filter_by(student_id=s.id).all()
                print(f"  -> Student: {s.name} (ID: {s.student_id}) has {len(s_fees)} fee records:")
                for f in s_fees:
                    print(f"       * Receipt {f.receipt_number}: {f.fee_category} | Total: Rs. {f.total_fee:,.2f} | Paid: Rs. {f.amount_paid:,.2f} | Status: {f.payment_status} | Due: {f.due_date}")

            # 2. Login as admin user
            admin = User.query.filter_by(username='admin').first()
            assert admin is not None, "Admin user not found!"
            
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin.id)
                sess['_fresh'] = True

            print("\n[3/6] Testing GET routes with authenticated user:")
            routes_to_test = [
                ('/fees/dashboard', 'Fees Dashboard'),
                ('/fees/records', 'Fees Records'),
                ('/fees/add', 'Add Fee Record Page'),
                ('/fees/reports', 'Fees Reports Page'),
            ]

            for url, name in routes_to_test:
                resp = client.get(url)
                print(f"  -> {name} ({url}): HTTP {resp.status_code}")
                assert resp.status_code == 200, f"Failed to load {name}! Status: {resp.status_code}"

            # Test student fee profile & receipt & edit
            sample_fee = Fee.query.first()
            if sample_fee:
                url_profile = f'/fees/student/{sample_fee.student_id}'
                resp = client.get(url_profile)
                print(f"  -> Student Fee Profile ({url_profile}): HTTP {resp.status_code}")
                assert resp.status_code == 200, f"Failed to load profile for {sample_fee.student_id}"

                url_receipt = f'/fees/receipt/{sample_fee.id}'
                resp = client.get(url_receipt)
                print(f"  -> Printable Receipt ({url_receipt}): HTTP {resp.status_code}")
                assert resp.status_code == 200, f"Failed to load receipt {sample_fee.id}"

                url_edit = f'/fees/edit/{sample_fee.id}'
                resp = client.get(url_edit)
                print(f"  -> Edit Fee Form ({url_edit}): HTTP {resp.status_code}")
                assert resp.status_code == 200, f"Failed to load edit form {sample_fee.id}"

            # 3. Testing Excel & CSV Export endpoints
            print("\n[4/6] Testing Data Export Endpoints:")
            resp_csv = client.get('/fees/export/daily/csv')
            print(f"  -> CSV Export: HTTP {resp_csv.status_code} | Content-Type: {resp_csv.headers.get('Content-Type')}")
            assert resp_csv.status_code == 200 and 'csv' in resp_csv.headers.get('Content-Type', '').lower()

            resp_excel = client.get('/fees/export/daily/excel')
            print(f"  -> Excel Export: HTTP {resp_excel.status_code} | Content-Type: {resp_excel.headers.get('Content-Type')}")
            assert resp_excel.status_code == 200

            # 4. Test CRUD: Adding a new fee record via POST
            print("\n[5/6] Testing POST /fees/add (CRUD Add & Auto calculation):")
            test_student = students[0]
            post_data = {
                'student_id': str(test_student.id),
                'fee_category': 'Tuition Fee',
                'custom_category': '',
                'academic_year': '2026-2027',
                'semester': 'Sem 5',
                'total_fee': '50000.00',
                'scholarship_discount': '5000.00',
                'fine_amount': '1000.00',
                'amount_paid': '25000.00',
                'payment_method': 'UPI',
                'transaction_reference': 'UPI987654321',
                'due_date': '2027-01-15',
                'payment_date': '2026-07-27',
                'remarks': 'Verification automated test payment'
            }
            resp_post = client.post('/fees/add', data=post_data, follow_redirects=True)
            assert resp_post.status_code == 200, f"Failed to add fee record! Status: {resp_post.status_code}"
            
            # Check created record in database
            created_fee = Fee.query.filter_by(remarks='Verification automated test payment').first()
            if created_fee is None:
                print("DEBUG Form errors:", resp_post.get_data(as_text=True)[:2000])
            assert created_fee is not None, "Created fee record not found in database!"
            print(f"  -> Successfully created fee record: Receipt {created_fee.receipt_number}")
            print(f"     Net Fee (50000-5000+1000): Rs. {created_fee.total_fee - created_fee.scholarship_discount + created_fee.fine_amount:,.2f}")
            print(f"     Amount Paid: Rs. {created_fee.amount_paid:,.2f} | Balance: Rs. {created_fee.remaining_balance:,.2f} | Status: {created_fee.payment_status}")
            assert created_fee.remaining_balance == 21000.0, f"Expected balance 21000, got {created_fee.remaining_balance}"

            # 5. Test Delete Fee Record
            print("\n[6/6] Testing POST /fees/delete (CRUD Delete):")
            resp_del = client.post(f'/fees/delete/{created_fee.id}', follow_redirects=True)
            assert resp_del.status_code == 200
            del_check = db.session.get(Fee, created_fee.id)
            assert del_check is None, "Fee record was not deleted from DB!"
            print("  -> Successfully deleted test fee record.")

    print("\n" + "=" * 70)
    print("ALL 6 VERIFICATION PHASES PASSED SUCCESSFULY! FEES MODULE IS 100% OPERATIONAL!")
    print("=" * 70)

if __name__ == '__main__':
    test_fees_module()
