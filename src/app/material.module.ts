// src/app/material.module.ts
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  exports: [
    MatButtonModule,
    MatCardModule,
    MatToolbarModule,
    MatExpansionModule,
    MatTableModule
  ]
})
export class MaterialModule {}
