import { Component, OnInit } from '@angular/core';
import samples_docs from "../../assets/samples.json";

export class SampleNode {

    public get file(): string {
        return this._file;
    }
    public get path(): string {
        return this._path;
    }
    constructor(protected _file: string, protected _path: string) {
    }
}

@Component({
	selector: 'samples-component',
	templateUrl: './samples.component.html',
	styleUrls: ['./samples.component.scss']
})
export class SamplesComponent implements OnInit {

	Samples: SampleNode[] = [];
	SelectedSample: string = '';
	SelectedContent: string = '';

	constructor() { }

	ngOnInit() {
		for (let key of Object.keys(samples_docs)) {
			this.Samples.push( new SampleNode(this.getFileFromPath(key), key));
		}

		this.Samples.sort((a, b) => a.file < b.file ? -1 : a.file > b.file ? 1 : 0);

		this.SelectedSample = this.Samples[0].path;
		this.SelectedContent = samples_docs[this.SelectedSample];
	}

	onSampleSelect(e: MouseEvent, item: any) {
		e.stopPropagation();
		this.SelectedSample = item.path;
		this.SelectedContent = samples_docs[this.SelectedSample];
	}

	getFileFromPath(path: string): string {
		const split = path.split('.');
		const count = split.length;
		return split[count - 2] + '.' + split[count - 1];
	}
}
