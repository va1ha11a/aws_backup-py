import unittest, datetime
from VolSnap.utils import isDueDays, isDueHours, isDueWeeks, isDueMonths, isDueYears

class IsDueHourTestCase(unittest.TestCase):
    hourly_backups = [(datetime.datetime(2013,1,1,21,30), "id-1234"),
                     (datetime.datetime(2013,1,1,22,30), "id-1235"),
                     (datetime.datetime(2013,1,1,23,30), "id-1236"),
                     (datetime.datetime(2013,1,2,0,30), "id-1237"),
                     (datetime.datetime(2013,1,2,1,30), "id-1238"),
                     (datetime.datetime(2013,1,2,2,30), "id-1239"),
                     (datetime.datetime(2013,1,2,3,30), "id-12340"),
                     ]   
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Hours_Not_Due_list(self):
        now = datetime.datetime(2013,1,2,4,29)
        due = isDueHours(self.hourly_backups, 1, now)
        self.assertEqual(due, False, "Showing Hourly due when it is not due.")

    def test_Hours_Due_list(self):
        now = datetime.datetime(2013,1,2,4,30)
        due = isDueHours(self.hourly_backups, 1, now)
        self.assertEqual(due, True, "Showing Hourly Not due when it is due.")
        
    def test_Hours_Due2_list(self):
        now = datetime.datetime(2013,1,2,4,31)
        due = isDueHours(self.hourly_backups, 1, now)
        self.assertEqual(due, True, "Showing Hourly Not due when it is due.")
        
class IsDueDayTestCase(unittest.TestCase):
    
    daily_backups = [(datetime.datetime(2013,1,1), "id-1234"),
                     (datetime.datetime(2013,1,2), "id-1235"),
                     (datetime.datetime(2013,1,3), "id-1236"),
                     (datetime.datetime(2013,1,4), "id-1237"),
                     (datetime.datetime(2013,1,5), "id-1238"),
                     (datetime.datetime(2013,1,6), "id-1239"),
                     (datetime.datetime(2013,1,7), "id-12340"),
                     ]
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_Days_Due_list(self):
        now = datetime.datetime(2013,1,8, 12)
        due = isDueDays(self.daily_backups, 1, now)
        self.assertEqual(due, True, "Showing days not due when it should be due")

    def test_Days_Not_Due_list(self):
        now = datetime.datetime(2013,1,7, 12)
        due = isDueDays(self.daily_backups, 1, now)
        self.assertEqual(due, False, "Showing days due when it should not be due")
                
    def test_2Days_Due_list(self):
        now = datetime.datetime(2013,1,8, 12)
        due = isDueDays(self.daily_backups, 2, now)
        self.assertEqual(due, False, "Showing days due when it should not be due")
        
    def test_2Days_Not_Due_list(self):
        now = datetime.datetime(2013,1,9, 12)
        due = isDueDays(self.daily_backups, 2, now)
        self.assertEqual(due, True, "Showing days due when it should be due")
        
class IsDueWeekTestCase(unittest.TestCase):
    hourly_backups = [(datetime.datetime(2013,1,1,0,30), "id-1234"),
                     (datetime.datetime(2013,1,8,0,30), "id-1235"),
                     (datetime.datetime(2013,1,15,0,30), "id-1236"),
                     ]   
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Weeks_Not_Due_list(self):
        now = datetime.datetime(2013,1,21,0,30)
        due = isDueWeeks(self.hourly_backups, 1, now)
        self.assertEqual(due, False, "Showing Weekly due when it is not due.")
        
    def test_Weeks_Due_list(self):
        now = datetime.datetime(2013,1,22,0,30)
        due = isDueWeeks(self.hourly_backups, 1, now)
        self.assertEqual(due, True, "Showing Weekly not due when it is due.")       

class IsDueMonthTestCase(unittest.TestCase):
    hourly_backups = [(datetime.datetime(2012,11,1,0,30), "id-1234"),
                     (datetime.datetime(2012,12,1,0,30), "id-1235"),
                     (datetime.datetime(2013,1,1,0,30), "id-1236"),
                     ]   
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Months_Not_Due_list(self):
        now = datetime.datetime(2013,1,31,0,30)
        due = isDueMonths(self.hourly_backups, 1, now)
        self.assertEqual(due, False, "Showing Monthly due when it is not due.")
        
    def test_Months_Due_list(self):
        now = datetime.datetime(2013,2,1,0,30)
        due = isDueMonths(self.hourly_backups, 1, now)
        self.assertEqual(due, True, "Showing Monthly not due when it is due.")     

    def test_2Months_Not_Due_list(self):
        now = datetime.datetime(2013,2,28,0,30)
        due = isDueMonths(self.hourly_backups, 2, now)
        self.assertEqual(due, False, "Showing Monthly due when it is not due.")
        
    def test_2Months_Due_list(self):
        now = datetime.datetime(2013,3,1,0,30)
        due = isDueMonths(self.hourly_backups, 2, now)
        self.assertEqual(due, True, "Showing Monthly not due when it is due.")
        
        
class IsDueYearTestCase(unittest.TestCase):
    hourly_backups = [(datetime.datetime(2010,1,1,0,30), "id-1234"),
                     (datetime.datetime(2011,1,1,0,30), "id-1235"),
                     (datetime.datetime(2012,1,1,0,30), "id-1236"),
                     ]   
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Months_Not_Due_list(self):
        now = datetime.datetime(2013,1,1,0,29)
        due = isDueYears(self.hourly_backups, 1, now)
        self.assertEqual(due, False, "Showing Monthly due when it is not due.")
        
    def test_Months_Due_list(self):
        now = datetime.datetime(2013,1,1,0,30)
        due = isDueYears(self.hourly_backups, 1, now)
        self.assertEqual(due, True, "Showing Monthly not due when it is due.")     
