import { Component, OnInit, Input } from '@angular/core';
import {Sort} from '@angular/material/sort';


import { RestRequestService } from '../rest-request.service'
import { AppRoutingModule } from '../app-routing.module';

@Component({
  selector: 'app-expenses',
  templateUrl: './expenses.component.html',
  styleUrls: ['./expenses.component.css']
})
export class ExpensesComponent implements OnInit {
  constructor(private restRequestService:RestRequestService) {   
  }
  
  uuid: any
  description: String
  created_at: String
  amount: Number
  currency: String
  employee: any
  expense_approved: any

  expensesAvailable
  inprogress: Boolean
  total: Number
  allExpenses
  
  backendUnavailable = false
  sortedExpenses

  ngOnInit() {
    this.inprogress = true
    this.restRequestService.getRequest(undefined, "expenses", undefined).subscribe(
      expenses => {
        this.total = 0
        if (Object.keys(expenses).length > 0) {
            this.expensesAvailable = true
            this.total = Object.keys(expenses).length
        }
        this.allExpenses = expenses
        console.log(this.allExpenses)
        this.inprogress = false
      },
      failure => {
        this.inprogress = true
        console.log("Failure: "+ JSON.stringify(failure))
        
        if (failure.status == 0) {
          this.backendUnavailable = true
        }
        this.inprogress = false
      }
    )
  }

  

  sortExpenses(sort: Sort) {
    const data = this.allExpenses.slice()


    this.allExpenses = data.sort((a, b) => {
      const isAsc = sort.direction === 'asc';
      switch (sort.active) {
        case 'uuid': return compare(a.uuid, b.uuid, isAsc);
        case 'description': return compare(a.description, b.description, isAsc);
        case 'created_at': return compare(a.created_at, b.created_at, isAsc);
        case 'amount': return compare(a.amount, b.amount, isAsc);
        case 'currency': return compare(a.currency, b.currency, isAsc);
        case 'approval': return compare(a.expense_approved, b.expense_approved, isAsc);
        case 'employee': return compare(a.employee.first_name + " " + a.employee.last_name, 
        b.employee.first_name + " " + b.employee.last_name, isAsc);
        default: return 0;
      }
    });

  }

  processExpense(index, expense) {
    var expenseUuid = expense.uuid
    var approved = expense.expense_approved

    console.log(expense)
    
    var approvalTransition = ""
    var processExpenseResponse: any;

    if (approved) {
      approvalTransition = "decline" 
    } else {
      approvalTransition = "approve" 
    }
    if (confirm(approvalTransition + " the expense claim " + expenseUuid + " ?")) {
      console.log("ok")
    } else {
      console.log("not ok")
      return false
    }

    this.restRequestService.postRequest(undefined, undefined, "expenses", expenseUuid + "/" + approvalTransition).subscribe(
      response => {
        processExpenseResponse = response
        
        if (processExpenseResponse["transaction_approval"] == "approve") {
            this.allExpenses[index]["expense_approved"] = true
        }

        if (processExpenseResponse["transaction_approval"] == "decline") {
            this.allExpenses[index]["expense_approved"] = false
        }
      },
      error => {
        alert("Sorry, there was an error processing your request.")
        console.log(error)
      }
    )
  }

  public trackExpense(index, expense) {
    return expense
  }
}

function compare(a: number | string, b: number | string, isAsc: boolean) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
