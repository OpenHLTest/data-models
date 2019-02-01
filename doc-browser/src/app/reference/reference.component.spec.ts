import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleTreeviewComponent } from './module-treeview.component';

describe('ModuleTreeviewComponent', () => {
  let component: ModuleTreeviewComponent;
  let fixture: ComponentFixture<ModuleTreeviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModuleTreeviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModuleTreeviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
