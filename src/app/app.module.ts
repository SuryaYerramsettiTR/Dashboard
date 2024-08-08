import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {AppComponent} from './app.component';
import {RepoDashboardComponent} from './repo-dashboard/repo-dashboard.component';
import {RepoCardComponent} from './repo-card/repo-card.component';
import {MaterialModule} from "./material.module";

@NgModule({
  declarations: [
    AppComponent,
    RepoDashboardComponent,
    RepoCardComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
