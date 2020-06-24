#include <iostream>
using namespace std;
class IntCell{
public:
    explicit IntCell( int initValue = 0){
	storeValue = new int(initValue);
	//only initialize storevalue rather than *storevalue
    }
    int read() const{
	return *storeValue;
    }
    void write(int newValue){
	*storeValue = newValue;
    }
private:
    int * storeValue;   
};

class IntCellRe{
public:
    explicit IntCellRe( int initValue = 0){
	storeValue = new int(initValue);
	//only initialize storevalue rather than *storevalue
    }
    ~IntCellRe(){delete storeValue;}

    IntCellRe(const IntCellRe & rhs){
	// use const and it will copy Class???
	// `IntCellRe b = a` calls this constructor
	storeValue = new int{ *rhs.storeValue}; // ??? with *
    }
    IntCellRe(IntCellRe && rhs): storeValue{rhs.storeValue}
	{rhs.storeValue = nullptr;}

    IntCellRe & operator= (const IntCellRe & rhs){
	
    }
    int read() const{
	return *storeValue;
    }
    void write(int newValue){
	*storeValue = newValue;
    }
private:
    int * storeValue;   
};

int main(){
    IntCell a{4};
    IntCell b = a;
    IntCell c;

    c = b;
    a.write(6);
    cout << a.read() << endl << b.read() << endl << c.read() <<endl;
    return 0;
}
