
import db


def spaceTime(tablesName, field, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2):
    args = [tablesName, field, dt1, dt2, lat1, lat2, lon1, lon2, depth1, depth2]
    query = 'EXEC uspSpaceTime ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
    df = db.dbFetchStoredProc(query, args)   
    return df