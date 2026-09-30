import unittest
from analyze import analyze

class AnalysisTests(unittest.TestCase):
    def test_conversion_owner_filter_and_null_doses(self):
        # Arbitrary synthetic IDs and component quantities, not personal mappings.
        units=[{'id':101,'name':'Adderall XR','doseComponents':[{'substanceName':'Amphetamine','substanceUnit':'mg','dose':10}]},
               {'id':102,'name':'Adderall IR','doseComponents':[{'substanceName':'Amphetamine','substanceUnit':'mg','dose':4}]}]
        def event(uid, dose, consumer=None):
            return {'customUnitId':uid,'dose':dose,'consumerName':consumer,'administrationRoute':'ORAL','time':946684800000}
        result=analyze({'customUnits':units,'experiences':[{'ingestions':[event(101,1),event(102,.5),event(102,None),event(101,2,'Other')]}]})
        self.assertEqual(result['ownIngestions'],3)
        self.assertEqual(result['otherIngestions'],1)
        self.assertEqual(result['bothDays'],1)
        self.assertEqual(result['unknownDose'],1)
        self.assertEqual(result['monthly'][0]['XR'],10)
        self.assertEqual(result['monthly'][0]['IR'],2)
        self.assertEqual(result['monthly'][0]['IR_count'],2)
    def test_no_adderall(self):
        result=analyze({'experiences':[]})
        self.assertEqual(result['adderallEvents'],0)
        self.assertIsNone(result['first'])

if __name__=='__main__': unittest.main()
