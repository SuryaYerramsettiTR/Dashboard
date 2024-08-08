import { Component, OnInit } from '@angular/core';
import { RepoDataService } from '../repo-data.service';

@Component({
  selector: 'app-repo-dashboard',
  templateUrl: './repo-dashboard.component.html',
  styleUrls: ['./repo-dashboard.component.css']
})
export class RepoDashboardComponent implements OnInit {
  repos: any[] = [];

  constructor(private repoDataService: RepoDataService) {}

  ngOnInit(): void {
    this.fetchData();
    setInterval(() => this.fetchData(), 300000); // Refresh every 5 minutes
  }

  fetchData(): void {
    this.repoDataService.getReposData().subscribe(data => {
      this.repos = data;
    });
  }
}
