import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import model_docs from "../../assets/documentation.json";
import { TreeComponent, TreeModel, TreeNode, ITreeOptions } from 'angular-tree-component';

enum eSelectionType {
    none = <any>'none',
    info = <any>'info',
    property = <any>'property',
    method = <any>'method',
}

@Component({
    selector: 'reference-component',
    templateUrl: './reference.component.html',
    styleUrls: ['./reference.component.scss']
})

export class ReferenceComponent implements OnInit, AfterViewInit {

	@ViewChild('tree') treeComponent: TreeComponent;
	private _options: ITreeOptions;
	private _yangName: any;
	private _yangKeyword: any;
	private _yangPath: any;
	private _yangListKey: any;
	private _yangDescription: any;
	private _yangWriteable: any;
	private _yangType: any;

    constructor() { 
		this._options = {
		};
	}

    ngOnInit() {
		
    }

	ngAfterViewInit() {
		this.treeComponent.treeModel.getFirstRoot().setActiveAndVisible();
	}

	public get options(): any {
		return this._options;
	}

	public get nodes(): any {
		return model_docs;
	}

	public onActivate(event: any) {
		this._yangPath = event.node.data._path;
		this._yangName = event.node.data.name;
		this._yangKeyword = event.node.data._keyword;
		this._yangListKey = event.node.data._key;
		this._yangDescription = event.node.data._description;
		this._yangWriteable = event.node.data._writeable;
		this._yangType = event.node.data._type;
	}

	public get yangName(): any {
		return this._yangName;
	}
    public get yangKeyword(): any {
        return this._yangKeyword;
    }
    public get yangDescription(): any {
        return this._yangDescription;
	}
	public get yangPath(): any {
		return this._yangPath;
	}
	public get yangListKey(): any {
		return this._yangListKey;
	}
	public get yangWriteable(): any {
		return this._yangWriteable;
	}
	public get yangType(): any {
		return this._yangType;
	}
	public get restGet(): any {
		let restStmt = 'GET http://<ipaddress[:port]>/restconf/data/';
		if (this._yangKeyword === 'list')
			restStmt += this._yangPath + '=<' + this._yangListKey + '>';
		else
			restStmt += this._yangPath;
		return restStmt;
	}
	public get restPost(): any {
		return 'POST http://<ipaddress[:port]>/restconf/data/' + this._yangPath;
	}
	public get restPatch(): any {
		let restStmt = 'PATCH http://<ipaddress[:port]>/restconf/data/';
		if (this._yangKeyword === 'list')
			restStmt += this._yangPath + '=<' + this._yangListKey + '>';
		else
			restStmt += this._yangPath;
		return restStmt;	
	}
	public get restDelete(): any {
		let restStmt = 'DELETE http://<ipaddress[:port]>/restconf/data/';
		if (this._yangKeyword === 'list')
			restStmt += this._yangPath + '=<' + this._yangListKey + '>';
		else
			restStmt += this._yangPath;
		return restStmt;	
	}
}
