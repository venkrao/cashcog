import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RestRequestService {

  constructor( private http: HttpClient) {

   }

  postEndPoints = {
    "expenses": {
      endpoint: "http://127.0.0.1:8000/expenses/",
      urlparams: undefined
      }
    }

  getEndPoints = {
    "expenses": {
        endpoint: "http://127.0.0.1:8000/expenses/",
        urlparams: undefined
    },
  }


  public postRequest(httpRequestHeaders:any, httpRequestData:any, httpEndPoint:any, urlParam: any) {

    if (urlParam != undefined) {
      this.endpoint = this.postEndPoints[httpEndPoint]["endpoint"] + urlParam
    } else {
      this.endpoint = this.postEndPoints[httpEndPoint]["endpoint"]
    }

    if (this.postEndPoints[httpEndPoint]["urlparams"]) {
      this.endpoint = this.endpoint + "/" + this.postEndPoints[httpEndPoint]["urlparams"]
    }
  
   console.log("sending post request to: " + httpEndPoint + ": " + this.endpoint)

   console.log("composed request headers " + JSON.stringify(httpRequestHeaders))
   return this.http.post(this.endpoint, httpRequestData, httpRequestHeaders)
  }

  private endpoint: any;

  public getRequest(httpRequestHeaders:any, httpEndPoint:any, urlParam:any ) {

    if (urlParam != undefined) {
      this.endpoint = this.getEndPoints[httpEndPoint]["endpoint"] + "/" + urlParam
    } else {
      this.endpoint = this.getEndPoints[httpEndPoint]["endpoint"]
    }

    if (this.getEndPoints[httpEndPoint]["urlparams"]) {
      this.endpoint = this.endpoint + "/" + this.getEndPoints[httpEndPoint]["urlparams"]
    }

    console.log("sending get request to: " + httpEndPoint + ": " + this.endpoint)

    console.log("composed request headers " + JSON.stringify(httpRequestHeaders))
    return this.http.get(this.endpoint, httpRequestHeaders)
  }
}
