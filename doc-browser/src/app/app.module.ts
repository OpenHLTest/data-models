import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { AceEditorModule } from 'ng2-ace-editor';
import { TreeModule } from 'angular-tree-component';
import { ReferenceComponent } from './reference/reference.component';
import { SamplesComponent } from './samples/samples.component';
import { CodeviewerComponent } from './codeviewer/codeviewer/codeviewer.component';

@NgModule({
	declarations: [
		AppComponent,
		ReferenceComponent,
		SamplesComponent,
		CodeviewerComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		AceEditorModule,
		TreeModule.forRoot(),
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
