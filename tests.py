import unittest
#import requests

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):

    def test_dummy(self):
        self.assertEqual(fun(3), 4)

        #def test_api_call(self):
        #r = requests.get("http://0.0.0.0:5000")
        #self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()