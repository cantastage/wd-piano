import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { API_URL } from 'src/env';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { VideoUrlObject } from './videoUrlObject';
import { SimulationParameters } from './model/SimulationParameters';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private HTTPOptions = {
    headers: new HttpHeaders({
      'Accept': 'video/mp4'
    }),
    'responseType': 'blob' as 'json'
  }

  // public url: Observable<VideoUrlObject> = of({ 'videoURL': ''});

  constructor(private http: HttpClient) { }

  getVideo(): Observable<VideoUrlObject> {
    return this.http.get<VideoUrlObject>(API_URL + '/video')
      .pipe(
        map(obj => obj),
        // TODO add error management
      )
  }

  getVideoFile(): Observable<File> {
    return this.http.get<File>(API_URL + '/video')
  }

  downloadVideo(): Observable<any> {
    return this.http.get<any>(API_URL + '/video', this.HTTPOptions)
      .pipe(
        catchError(this.handleError<any>('ERRORE AIUTOOO'))
      );
  }

  runSimulation(simulationParams: SimulationParameters): Observable<any> {  
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    const body = JSON.stringify(simulationParams);
    return this.http.post<any>(API_URL + '/simulation', body, { 'headers': headers })
      .pipe(
        catchError(this.handleError<any>('ERRORE AIUTOOO'))
      );
  }

  /**
   * Handle Http operation that failed. Taken from Angular Tour of Heroes
   * Let the app continue.
   *
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
