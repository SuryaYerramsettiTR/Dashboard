import { TestBed } from '@angular/core/testing';

import { RepoDataService } from './repo-data.service';

describe('RepoDataService', () => {
  let service: RepoDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RepoDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
