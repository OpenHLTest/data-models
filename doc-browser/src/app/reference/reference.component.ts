import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import model_docs from "../../assets/documentation.json";
import { TreeComponent, TreeModel, TreeNode, ITreeOptions } from 'angular-tree-component';


@Component({
	selector: 'reference-component',
	templateUrl: './reference.component.html',
	styleUrls: ['./reference.component.scss']
})

export class ReferenceComponent implements OnInit, AfterViewInit {

	@ViewChild('tree') treeComponent: TreeComponent;
	private _options: ITreeOptions;
	private _docs: Array<any>;
	private _currentDocNode: any;
	public YangName: any;
	public YangKeyword: any;
	public YangPath: any;
	public YangListKey: any;
	public YangDescription: any;
	public YangWriteable: any;
	public YangType: any;
	public YangPresence: any;
	public YangEnums: Array<any>;
	public YangLeafRefPaths: Array<string>;
	public YangStatus: any;
	public YangUnsupportedFeatures: Array<string>;
	public YangConstraint: any;

	constructor() {
		this._options = {
		};
	}

	ngOnInit() {
		this._docs = Array();
		//this.sort(this._docs, model_docs);
		this._docs = model_docs;
	}

	private sort(sortedDocs: Array<any>, unsortedDocs: Array<any>): void {
		if (sortedDocs && unsortedDocs) {
			for (let item of unsortedDocs.sort((a, b) => a.name.localeCompare(b.name))) {
				let copy = Object.create(item);
				copy['children'] = Array();
				sortedDocs.push(copy);
				this.sort(copy['children'], item['children'])
			}
		}
	}

	ngAfterViewInit() {
		this.treeComponent.treeModel.getFirstRoot().setActiveAndVisible().expand();
	}

	public get options(): any {
		return this._options;
	}

	public get nodes(): any {
		return this._docs;
	}

	public onActivate(event: any) {
		this._currentDocNode = event.node;
		this.YangPath = event.node.data._path;
		this.YangName = event.node.data.name;
		this.YangKeyword = event.node.data._keyword;
		this.YangListKey = event.node.data._key;
		this.YangDescription = event.node.data._description;
		this.YangWriteable = event.node.data._writeable;
		this.YangType = event.node.data._type;
		this.YangEnums = event.node.data._enums;
		this.YangPresence = event.node.data._presence;
		this.YangLeafRefPaths = event.node.data._leafref_paths;
		this.YangStatus = event.node.data._status;
		this.YangUnsupportedFeatures = event.node.data._unsupported_feature;
		this.YangConstraint = event.node.data._constraint;
	}

	public get isParentAnOperation(): boolean {
		let currentNode = this._currentDocNode;
		while (currentNode && currentNode.parent) {
			switch (currentNode.data._keyword) {
				case 'action':
				case 'rpc':
					return true;
			}
			currentNode = currentNode.parent;
		}
		return false;
	}
	public get restGet(): any {
		if (this.isParentAnOperation) {
			return undefined;
		}
		let restStmt = 'GET http://<ipaddress[:port]>/restconf/data/';
		if (this.YangKeyword === 'list')
			restStmt += this.YangPath + '=<' + this.YangListKey + '>';
		else
			restStmt += this.YangPath;
		switch (this.YangKeyword) {
			case 'module':
			case 'rpc':
			case 'action':
				return undefined;
			case 'list':
			case 'container':
				restStmt += '?depth=1';
				break;
			default:
				break;
		}
		return restStmt;
	}
	public get restPost(): any {
		switch (this.YangKeyword) {
			case 'list':
				let restStmt = 'POST http://<ipaddress[:port]>/restconf/data/'
				restStmt += this.YangPath;
				restStmt += '=<' + this.YangListKey + '>';
				restStmt += '\n';
				restStmt += 'Content-Type: application/json\n\n';
				let payload: string = '';
				payload = '';
				for (let child of this._currentDocNode.data.children) {
					switch (child['_keyword']) {
						case 'leaf':
						case 'leaf-list':
							payload += `\t"${child['name']}": <${child['_type']}>,\n`;
							break;
						default:
							break;
					}
				}
				if (payload.length > 0) {
					return restStmt + `{\n${payload.substr(0, payload.length - 2)}\n}`;
				} else {
					return undefined;
				}
			default:
				return undefined;
		}
	}
	public get restPatch(): any {
		switch (this.YangKeyword) {
			case 'list':
			case 'container':
				let restStmt = 'PATCH http://<ipaddress[:port]>/restconf/data/'
				restStmt += this.YangPath;
				if (this.YangKeyword === 'list') {
					restStmt += '=<' + this.YangListKey + '>';
				}
				restStmt += '\n';
				restStmt += 'Content-Type: application/json\n\n';
				let payload: string = '';
				payload = '';
				for (let child of this._currentDocNode.data.children) {
					switch (child['_keyword']) {
						case 'leaf':
						case 'leaf-list':
							if (child['name'] !== this.YangListKey) {
								payload += `\t"${child['name']}": <${child['_type']}>,\n`;
							}
							break;
						default:
							break;
					}
				}
				if (payload.length > 0) {
					return restStmt + `{\n${payload.substr(0, payload.length - 2)}\n}`;
				} else {
					return undefined;
				}
			default:
				return undefined;
		}
	}
	public get restDelete(): any {
		switch (this.YangKeyword) {
			case 'list':
				return `DELETE http://<ipaddress[:port]>/restconf/data/${this.YangPath}=<${this.YangListKey}>`;
			default:
				return undefined;
		}
	}
	public get restOperation(): any {
		let restStmt: string = '';
		switch (this.YangKeyword) {
			case 'action':
				restStmt = `POST http://<ipaddress[:port]>/restconf/data/${this.YangPath}`;
				break;
			case 'rpc':
				restStmt = `POST http://<ipaddress[:port]>/restconf/operations/${this.YangPath}`;
				break;
			default:
				return undefined;
		}
		// restStmt += '\n';
		// restStmt += 'Content-Type: application/json\n\n';
		// let payload: string = '';
		// payload = '';
		// for (let child of this._currentDocNode.children) {
		// 	if (child['_keyword'] === 'leaf' && child['name'] !== this.YangListKey) {
		// 		payload += `\t"${child['name']}": <${child['_type']}>,\n`;
		// 	}
		// }
		// if (payload.length > 0) {
		// 	return restStmt + `{\n${payload.substr(0, payload.length - 2)}\n}`;
		// }
		return restStmt;
	}

	private get ooPath(): string {
		let path: string = '';
		if (this.YangPath) {
			for (let item of this.YangPath.split('/')) {
				if (item === 'oht') {
					path = "OpenHlTest"
				} else {
					path += "." + item[0].toUpperCase() + item.substr(1)
				}
			}
		}
		return path;
	}
	private pythonName(name: string): string {
		if (name) {
			let camelCaseName = '';
			for (let piece of name.split('-')) {
				camelCaseName += piece.substr(0, 1).toUpperCase() + piece.substr(1);
			}
			return camelCaseName;
		} else {
			return '';
		}
	}
	public get pythonClass(): string {
		return `class ${this.pythonName(this.YangName)}(Base):`;
	}
	public get pythonInit(): string {
		if (this.YangKeyword === 'module')
			return `def __init__(Transport):`;
		else
			return `def __init__(self, parent):`;
	}
	public get pythonClassProperties(): string {
		//for (let child of this.)
		return `${this.ooPath}.find(name=<value>)`;
	}
	public get pythonUpdate(): string {
		return `${this.ooPath}.update(name=<value>)`;
	}
	public get pythonDelete(): string {
		return `${this.ooPath}.delete(name=<value>)`;
	}
	public get pythonExecute(): string {
		return `${this.ooPath}.execute(name=<value>)`;
	}
}
