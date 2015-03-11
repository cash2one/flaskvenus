from venus import app

def testview():
    with app.test_request_context():
        print(url_for('login'))
        
if __name__ == '__main__':
    testview()

