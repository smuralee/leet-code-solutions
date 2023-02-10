class Node: 
    # mutable class 

    def __init__(self, val, next=None, random = None) -> None:
        self.val = int(val)
        self.next = next 
        self.random = random 


class solution: 
    # write a deep copy for the given singly linked list with random pointers 
    def __init__(self, visited:dict) -> None:
        self.visited = visited
        self.visited[None] = None

    def CopyRandomList(self, head:Node,): 

        """Method one: 
        Two passes, first pass we construct a placeholder (created from scratch)

        In the second pass, we link those place holders together 

        TC : O(N)
        SC : O(N)
        """
         
        # build place holders (unlinked)
        map_ = {}
        curr = head
        while curr: 
            map_[curr] = Node(curr.val)
            curr = curr.next
        map_[None] = None

        # linked the place holders
        curr = head 
        while curr: 
            print(curr.val)

            copyed = map_[curr] 
            copyed.next = map_[curr.next]
            copyed.random = map_[curr.random]

            curr = curr.next

        return map_[head]

    def copyRandomList_one_pass(self, head:Node) -> Node: 

        old = head 

        while old: 

            if old not in self.visited:
                self.visited[old] = Node(old.val)

            new = self.visited[old]

            if old.next not in self.visited: 
                self.visited[old.next] = Node(old.next.val)

            if old.random not in self.visited: 
                self.visited[old.random] = Node(old.random.val)

            new.next = self.visited[old.next]
            new.random = self.visited[old.random] 

            old = old.next 

        return self.visited[head]

    def copyRandomList_weaving(self, head: Node) -> Node:
        
        old = head 

        # create iterving nodes
        while old: 
            #print(old.val )
            tmp = old.next 
            old.next = Node(old.val) 
            old.next.next = tmp 

            old = old.next.next 

        curr = head 
        while curr: 

            curr.next:Node

            next_old = curr.next.next 

            curr.next.next = curr.next.next.next if curr.next.next else None
            curr.next.random = curr.random.next if curr.random else None

            curr = next_old

        return head.next if head else None


    def copyRandomList_recursive(self, head: Node) -> Node:
        
        if not head: 
            return None 

        if head in self.visited:
            return self.visited[head]

        # create the place holder
        #print(head)
        #print(head.val)
        new_head = Node(head.val, next=None, random=None)
        self.visited[head] = new_head 

        # update propeties 
        new_head.next = self.copyRandomList(head.next)
        new_head.random = self.copyRandomList(head.random)
        
        return new_head 



if  __name__ == "__main__": 


    n2 = Node(13, next=None, random=None)
    n1 = Node(7, next=n2, random=None)

    n1.random = n2 
    n2.random = n2 

    deep_copyed_head = solution().CopyRandomList(n1)







        

        
        


