import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, Observer} from "rxjs";
import {of} from 'rxjs'
import { catchError } from 'rxjs/operators'
import {HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class BbService {
  private url: String = 'http:localhost:8000'
  constructor(private http:HttpClient) { }
  getBbs(): Observable<Object[]> {
    return this.http.get<Object[]>(this.url + '/api/bbs/')
  }
  getBb(pk:Number):Observable<Object> {
    return this.http.get<Object>(this.url + '/api/bbs' + pk)
  }
  handleError() {
    //replaced Observable<Object> to Observable<any>
    return (error: any): Observable<any> => {
      window.alert(error.message);
      return of(null);
    }
  }
  addComment(bb:string, author:string, password:string, content:string): Observable<Object> {
    const comment = {'bb':bb, 'author':author, 'content':content};
    const options = {headers: new HttpHeaders(
        {'Content-Type': 'application/json',
                'Authorization': 'Basic' + window.btoa(author+ ':' + 'password')})}
    return this.http.post<Object>(this.url + '/api/bbs/' + bb + '/comments/', comment, options).pipe(catchError(this.handleError()))
  }
  getComment(pk: Number):Observable<Object[]> {
    return this.http.get<Object[]>(this.url + '/api/bbs/' + pk + '/comments/')
  }
}
