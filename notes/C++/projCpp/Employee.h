#pragma once
#include <string>
using namespace std;
namespace Records{
    const int kDefaultStartingSalary = 30000;

    class Employee
    {
    public:
	Employee(); // constructor has no type
	void promote(int raiseAmount = 1000); // default value exists in function declaration rather than function definition
	void demote(int demeritAmount = 1000);
	void hire();
	void fire();
	void display();
	
	void setFirstName(const string & firstName);
	const string & getFirstName() const;

	void setLastName(const string lastName);
	const string getLastName() const;

	void setEmployeeNumber(int employeeNumber);
	int getEmployeeNumber() const;

	void setSalary(int newSalary);
	int getSalary() const;

	bool getIsHired() const;

    private:
	string mFirstName;
	string mLastName;
	int mEmployeeNumber;
	int mSalary;
	bool mHired;
    };
}
