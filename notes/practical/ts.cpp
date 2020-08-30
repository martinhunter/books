#include <iostream>
#include <vector>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(NULL) {}
};


// ListNode* addTwoNumbers(ListNode* l1, ListNode* l2, int jinwei=0) {
//     ListNode elem(0);
//     ListNode* pt = elem;

//     ListNode* p1 = l1;
//     ListNode* p2 = l2;
//     while (p1 || p2) {

//     	pt.value = p1.val + p2.val;
//  		ListNode tp(pt.val);
//  		prev.next = &tp;
//  		p1 = p1->next;
//     	p2 = p2->next;
//     	pt.
//     }
// }



int main(){
	// ListNode L1(2);

	// ListNode n2(4);
	// L1.next = &n2;

	// ListNode n3(3);
	// n2.next = &n3;

	// ListNode n3(3);
	// n2.next = &n3;
	ListNode L1(2);
	L1->next = new ListNode(3);
	cout << L1.next->val;
	return 0;
}