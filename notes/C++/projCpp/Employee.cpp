#include <iostream>
#include "Employee.h"
using namespace std;
namespace Records{
    // the definition of constructor
    Employee::Employee()
	:mFirstName("")
	,mLastName("")
	,mEmployeeNumber(-1)
	,mSalary(kDefaultStartingSalary)
	,mHired(false)
    {}

    void Employee::promote(int raiseAmount){
	setSalary(getSalary() + raiseAmount);
    }
    void Employee::demote(int demeritAmount){
	setSalary(getSalary() - demeritAmount);
    }
    void Employee::hire(){
	mHired = true;
    }
    void EMployee::fire()
    {
	mHired = false;
    }
    void Employee::display() const
    {
	cout << "Employee: " << getLastName() << ", " << getFirstName() << endl;
	cout << "--------------" << endl;
	cout << (mHired? "Current Employee": "Former Employee") << endl;
	cout << "Employee Number: " << getEmployeeNumber() << endl;
	cout << "Salary: $" << getSalary() << endl;
	cout << "\n";
    }
    void Employee::setFirstName(const string& firstName)
    {
	mFirstName = firstName;
    }
    const string& Employee::getFirstName() const
    {
	return mFirstName;
    }
    int getSalary() const
    {
	return mSalary;
    }
    void setSalary(int newSalary){
	mSalary = newSalary;
    }
    int getEmployeeNumber() const
    {
	return mEmployeeNumber;
    }
    void setEmployeeNumber(int employeeNumber){
	mEmployeeNumber = employeeNumber;
    }

}
