// src/app/material.module.ts
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTableModule } from '@angular/material/table';
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import { MatTabsModule } from "@angular/material/tabs";
import {MatGridList, MatGridListModule, MatGridTile} from "@angular/material/grid-list";

@NgModule({
  exports: [
    MatButtonModule,
    MatCardModule,
    MatToolbarModule,
    MatExpansionModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatTabsModule,
    MatGridListModule
  ]
})
export class MaterialModule {}
