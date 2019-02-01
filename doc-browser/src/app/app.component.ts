import { Component, OnInit } from '@angular/core';


export enum Tabs {
	overview,
	apireference,
	license
};

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.scss']
})

export class AppComponent {
	title = 'app';
	CurrentTab: Tabs;
	TabTypes = Tabs;

	constructor() { }

	async ngOnInit() {
		this.CurrentTab = Tabs.overview;
	}	
}
