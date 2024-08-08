import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RepoDataService {
  private apiUrl = 'http://localhost:5000/api/data';

  constructor(private http: HttpClient) {}

  getReposData(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
