import { Component, Input, OnInit } from '@angular/core';
import { ChartOptions, ChartType } from 'chart.js';
@Component({
  selector: 'app-repo-card',
  templateUrl: './repo-card.component.html',
  styleUrls: ['./repo-card.component.css']
})
export class RepoCardComponent implements OnInit {
  @Input() repo: any;
  isLoading = true;
  displayedColumns: string[] = [ 'title', 'source', 'target', 'author', 'reviewer', 'link'];
  buildColumns: string[] = [ 'title', 'status', 'branch', 'commit', 'author', 'link']
  versionInfoArray: any[] = [];
  versionColumns: string[] = ['branch', 'commonLib', 'wijmo', 'coreComponents'];
  // Chart configuration
  chartOptions: ChartOptions = {
    responsive: true,
  };
  chartLabels: any[] = ['Open PRs', 'Builds', 'Recently Closed PRs'];
  chartType: ChartType = 'bar';
  chartLegend = true;
  chartData: any = [
    { data: [0, 0, 0], label: 'Metrics' }
  ];
  ngOnInit(): void {
    // Add type field to distinguish between PRs and Builds
   // this.repo.builds.forEach((build: any) => build.type = 'Build');
    this.isLoading = false;
    this.transformVersionInfo();
  }

  getLatestCommitsArray(latestCommits: any): any[] {
    return Object.keys(latestCommits).map(branch => ({
      branch,
      commit: latestCommits[branch]
    }));
  }

  transformVersionInfo(): void {
    if (this.repo && this.repo.version_info) {
      for (const branch in this.repo.version_info) {
        if (this.repo.version_info.hasOwnProperty(branch)) {
          this.versionInfoArray.push({
            branch: branch,
            versions: this.repo.version_info[branch]
          });
        }
      }
    }
  }
}
