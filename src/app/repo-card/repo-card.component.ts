import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-repo-card',
  templateUrl: './repo-card.component.html',
  styleUrls: ['./repo-card.component.css']
})
export class RepoCardComponent implements OnInit {
  @Input() repo: any;
  displayedColumns: string[] = ['type', 'title', 'source', 'target', 'author', 'link'];
  buildColumns: string[] = ['type', 'title', 'status', 'author', 'link'];

  ngOnInit(): void {
    // Add type field to distinguish between PRs and Builds
    this.repo.builds.forEach((build: any) => build.type = 'Build');
  }
}