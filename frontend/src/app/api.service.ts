import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { API_URL } from 'src/env';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { VideoUrlObject } from './videoUrlObject';
import { WDParam } from './model/wd-settings';
import { SpectralAnalysisParameters, SpectralFeatures } from './model/daap-features';

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


  constructor(private http: HttpClient) { }

  getVideo(): Observable<VideoUrlObject> {
    return this.http.get<VideoUrlObject>(API_URL + '/video')
      .pipe(
        map(obj => obj),
        // TODO add error management
      )
  }

  /**
   * 
   * @returns Piano keys data as json
   */
  getPianoKeys(): Observable<Array<any>> {
    return this.http.get<any>(API_URL + '/strings')
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

  /**
   * Update spectral feature plots
   * @param spectralParams spectral analysis parameters
   * @returns updated plot urls
   */
  public updatePlots(baseFilename: string, spectralParams: SpectralAnalysisParameters, plotVersionIndex: number): Observable<SpectralFeatures> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    const body = JSON.stringify({ baseFilename, spectralParams, plotVersionIndex: plotVersionIndex });
    return this.http.post<SpectralFeatures>(API_URL + '/plots', body, { 'headers': headers });
  }

  /**
   * Updates comparison plots
   * @param filenames 
   * @param spectralParams 
   * @param plotVersionIndex 
   * @returns 
   */
  public updateComparisonPlots(baseFilename: string, filenames: Array<string>, spectralParams: SpectralAnalysisParameters, plotVersionIndex: number): Observable<SpectralFeatures> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    const body = JSON.stringify({ baseFilename, filenames, spectralParams, plotVersionIndex });
    return this.http.post<SpectralFeatures>(API_URL + '/compare-plots', body, { 'headers': headers });
  }

  /**
   * Run WdPiano algorith
   * @param wdParams 
   * @param spectralParameters
   * @returns 
   */
  public runWDPiano(wdParams: Object, spectralParameters: SpectralAnalysisParameters, createVideo: boolean): Observable<any> {
    const headers = new HttpHeaders().set('Content-Type', 'application/json');
    const body = JSON.stringify({ wdParameters: wdParams, spectralParameters: spectralParameters, createVideo: createVideo });
    return this.http.post<any>(API_URL + '/simulation', body, { 'headers': headers });
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
