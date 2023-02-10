from collections import defaultdict 
class TimeMap:

    def __init__(self):

        self.value_store = {}
        self.time_store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:

        if key not in self.value_store: 
            self.value_store[key] = {}
            self.value_store[key][timestamp] = value

            self.time_store[key] = []
            self.time_store[key].append(timestamp)
        else:
            self.value_store[key][timestamp] = value 
            self.time_store[key].append(timestamp)
    
    def get(self, key: str, timestamp: int) -> str: 

        if key in self.value_store: 
            l = 0
            r = len(self.time_store[key])-1 
            res = 0
            while l<= r: 
                mid = (l+r)//2 
                #print(res, l, mid, r)
                if self.time_store[key][mid] > timestamp: 
                    r = mid - 1
                else: 
                    res = max(res, mid)
                    l = mid + 1 
                #print(res, l, mid, r)
            if self.time_store[key][res] > timestamp:
                return ""
            else:
                return self.value_store[key][self.time_store[key][res]]
        else: 
            return "" 

if __name__ == "__main__": 

    tm = TimeMap()

    tm.set('love','high',10)
    print(tm.value_store)

    tm.set('love','low',20)
    print(tm.value_store)

    print(tm.get('love',5))
    # print(tm.get('foo',3))
    # print(tm.get('foo2',3))

    # print(tm.set("foo", "bar2", 4))
    # print(tm.value_store)
    # print(tm.time_store)

    # print(tm.get('foo',4))
    # print(tm.get('foo',5))
    # print(tm.get('foo',6))