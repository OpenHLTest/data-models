import { Component, OnInit, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import model_docs from "../../assets/documentation.json";
import { TreeComponent, TreeModel, TreeNode, ITreeOptions } from 'angular-tree-component';
import { SplitComponent } from 'angular-split';
import { preserveWhitespacesDefault } from '@angular/compiler';


enum eDescriptionFormat {
	class,
	classProperty,
	leafProperty,
	operation
}

export interface IYangNode {
	name: string,
	id: number,
	children: IYangNode[],
	_keyword: string,
	_key: string,
	_path: string,
	_description: string,
	_writeable: boolean,
	_type: string,
	_type_pattern: string,
	_enums: Array<string>,
	_leafref_paths: Array<string>,
	_presence: boolean,
	_status: string,
	_unsupported_feature: Array<string>,
	_constraint: string,
	_python_class: string
}

export interface ILeafRefNode {
	sourceNode: TreeNode,
	targetNode: TreeNode
}

export enum Tabs {
	node,
	sample,
	class,
	restconf
};

@Component({
	selector: 'reference-component',
	templateUrl: './reference.component.html',
	styleUrls: ['./reference.component.scss']
})
export class ReferenceComponent implements OnInit, AfterViewInit {
	@ViewChild('splitter') _splitterComponent: SplitComponent;
	@ViewChild('tree') _treeComponent: TreeComponent;
	@ViewChild('getCode') _getCode: ElementRef;
	@ViewChild('postCode') _postCode: ElementRef;
	@ViewChild('patchCode') _patchCode: ElementRef;
	@ViewChild('deleteCode') _deleteCode: ElementRef;
	@ViewChild('operationCode') _operationCode: ElementRef;
	@ViewChild('sampleCode') _sampleCode: ElementRef;
	@ViewChild('pythonClass') _pythonClass: ElementRef;
	private _nextId: number = 1;
	private _options: ITreeOptions = {};
	private _docs: Array<IYangNode>;
	private _currentDocNode: TreeNode;
	private _postContent: any;
	private _patchContent: any;
	private YangNode: IYangNode;
	public _nodeLens: IYangNode;
	public YangDisplayNodes: IYangNode[];
	public CurrentTab: Tabs;
	public TabTypes = Tabs;
	private _state = {
		'hiddenNodeIds': {}
	};
	static PREAMBLE = 'https://ipaddress[:port]';

	constructor() {
		this._docs = model_docs;
		for (let rootNode of this._docs) {
			this.setState(rootNode);
		}
	}
	setState(docNode: any) {
		switch (docNode._keyword) {
			case 'leaf':
			case 'leaf-list':
			case 'input':
			case 'output':
				this._state['hiddenNodeIds'][docNode.id] = true;
				break;
			default:
				if (docNode['children']) {
					for (let childNode of docNode['children']) {
						this.setState(childNode);
					}
				}
				break;
		}
	}
	async ngOnInit() {
		this.CurrentTab = Tabs.node;
	}
	ngAfterViewInit() {
		setTimeout(() => {
			this._splitterComponent.direction = 'horizontal';
			this._splitterComponent.disabled = false;
			this._splitterComponent.gutterSize = 5;
			this._treeComponent.treeModel.setState(this._state);
			this._currentDocNode = this.rootNode;
			this.YangNode = this._currentDocNode.data;
			this._currentDocNode.setActiveAndVisible().expand();
		});
	}

	public get nextId(): number {
		return this._nextId++;
	}
	public get options(): any {
		return this._options;
	}
	public get nodes(): any {
		return this._docs;
	}
	public get rootNode(): TreeNode {
		return this._treeComponent.treeModel.getFirstRoot();
	}
	public onActivate(event: any) {
		if (event.node) {
			this._nextId = 1;
			this._currentDocNode = event.node;
			this.YangNode = this._currentDocNode.data;
			let displayNodes = [this.YangNode];
			if (this.YangNode.children) {
				for (let yangChildNode of this.YangNode.children) {
					if(this.isProperty(yangChildNode)) {
						displayNodes.push(yangChildNode);
					}
				}
			}
			this.YangDisplayNodes = displayNodes;
			this._currentDocNode.expand();
			this.setGetContent();
			this.setPatchContent();
			this.setPostContent();
			this.setDeleteContent();
			this.setOperationContent();
			this.setPythonSample();
			this.setPythonClass();
		}
	}
	public get header(): string {
		if (this.YangNode) {
			return `${this.YangNode._path}`;
		} else {
			return '';
		}
	}
	private makeHyperLink(dataNode: any): string {
		return `<span id='node${dataNode.id}'>${dataNode.name}</span>`;
	}
	private createHyperlink(nodeId: number, name: string): string {
		return `<span id='node${nodeId}'>${name}</span>`;
	}
	public gotoNode(nodeId: any) {
		if (nodeId) {
			let treeNode = this._treeComponent.treeModel.getNodeById(nodeId);
			this._nodeLens = treeNode.data;
		}
	}
	public get NodeLens(): IYangNode { 
		return this._nodeLens;
	}
	public closeNodeLens(event: any) {
		this._nodeLens = undefined;
	}

	public getRequest(method: string): string {
		let request: string = `${method} ${ReferenceComponent.PREAMBLE}/restconf/data`;
		let path: string = this.getPath(method !== 'POST');
		if (path.length !== 0) {
			request += `/oht:${path}`;
		}
		request += '\n';
		request += this.xapiHeader;
		return request;
	}
	public getPath(addFinalNode: boolean): string {
		let pieces: Array<string> = [];
		let docNode = this._currentDocNode;
		while (docNode) {
			let node: IYangNode = docNode.data;
			if (node._keyword === 'module') {
				break;
			}
			if (addFinalNode) {
				if (node._keyword === 'list') {
					let keyNode: IYangNode = node.children.find((child) => child.name === node._key);
					let nameAndKey = `${node.name}=${this.createHyperlink(keyNode.id, keyNode.name)}`;
					pieces.unshift(nameAndKey);
				} else {
					pieces.unshift(node.name);
				}
			} else {
				addFinalNode = true;
			}
			docNode = docNode.parent;
		}
		return pieces.join('/');
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
	public get hasGet(): boolean {
		return this.YangNode && !this.isMethod(this.YangNode) && this.YangNode._keyword !== 'module';
	}
	public get hasPost(): boolean {
		return this.isList(this.YangNode);	
	}
	public get hasPatch(): boolean {
		if (this.YangNode && this.YangNode.children)
		{
			switch (this.YangNode._keyword) {
				case 'list':
					let nonKeyNode = this.YangNode.children.find((c) => c.name !== this.YangNode._key && c._keyword === 'leaf' || c._keyword === 'leaf-list');
					return nonKeyNode !== undefined;
				case 'container':
					let childNode = this.YangNode.children.find((c) => c._keyword === 'leaf' || c._keyword === 'leaf-list');
					return childNode !== undefined;
				default:
					return false;
			}
		}
		return false;
	}
	public get hasDelete(): boolean {
		return this.isList(this.YangNode);		
	}
	public get hasOperation(): boolean {
		if (this.YangNode) {
			switch (this.YangNode._keyword) {
				case 'action':
				case 'rpc':
					return true;
				default:
					return false;
			}
		}
		return false;
	}
	public setPythonClass() {
		if (this.YangNode && this.YangNode._python_class) {
			this._pythonClass.nativeElement.innerHTML = this.YangNode._python_class;
			this.processElementRef(this._pythonClass)
		}
	}
	public setGetContent() {
		if (this.hasGet && this._getCode) {
			let restStmt = this.getRequest('GET');
			this._getCode.nativeElement.innerHTML = restStmt;
			this.processElementRef(this._getCode);
		}
		// 400 bad request (if not: json encoding, )
		// 401 unauthorized (x-api-key not present or invalid)
		// 404 not found (resource does not exist)
		// 405 method not allowed (get on an operation resource i.e. oht:authenticate)
	}
	public setPostContent(): boolean {
		if (this.hasPost && this._postCode) {
			switch (this.YangNode._keyword) {
				case 'list':
					let restStmt = this.getRequest('POST');
					restStmt += 'Content-Type: application/json\n\n';
					let payload: string = '';
					payload = '{\n';
					payload += `\t"oht:${this.YangNode.name}": {\n`;
					let payloadIds = [];
					for (let child of this._currentDocNode.data.children) {
						switch (child['_keyword']) {
							case 'leaf':
							case 'leaf-list':
								if (payloadIds.length > 0)
									payload += ',\n';
								payload += `\t\t"${this.makeHyperLink(child)}": ${child['_type']}`;
								payloadIds.push(child['id']);
								break;
							default:
								break;
						}
					}
					payload += '\n\t}\n';
					payload += '}';
					if (payloadIds.length > 0) {
						this._postContent = restStmt + payload;
						this._postCode.nativeElement.innerHTML = this._postContent;
						this.processElementRef(this._postCode);
					}
					break;
				default:
					break;
			}
			return true;
		}
		return false;
	}
	public setPatchContent(): boolean {
		if (this.hasPatch && this._patchCode) {
			switch (this.YangNode._keyword) {
				case 'list':
				case 'container':
					let restStmt = this.getRequest('PATCH');
					restStmt += 'Content-Type: application/json\n\n';
					let payload: string = '{\n';
					payload += `\t"oht:${this.YangNode.name}": {\n`;
					let payloadIds = [];
					for (let child of this.YangNode.children) {
						switch (child['_keyword']) {
							case 'leaf':
							case 'leaf-list':
								if (child['name'] !== this.YangNode._key) {
									if (payloadIds.length > 0)
										payload += ',\n';
									payload += `\t\t"${this.makeHyperLink(child)}": ${child['_type']}`;
									payloadIds.push(child['id']);
								}
								break;
							default:
								break;
						}
					}
					payload += '\n\t}\n';
					payload += '}';
					if (payload.length > 0) {
						this._patchContent = restStmt + payload;
						this._patchCode.nativeElement.innerHTML = this._patchContent;
						this.processElementRef(this._patchCode);
					}
					break;
				default:
					break;
			}
			return true;
		}
		return false;
	}
	public setDeleteContent() {
		if (this.hasDelete && this._deleteCode) {
			let restStmt = this.getRequest('DELETE');			
			this._deleteCode.nativeElement.innerHTML = restStmt;
			this.processElementRef(this._deleteCode);
		}
	}
	public setOperationContent() {
		if (this.hasOperation && this._operationCode) {
			let restStmt: string = '';
			switch (this.YangNode._keyword) {
				case 'action':
					restStmt = `POST ${ReferenceComponent.PREAMBLE}/restconf/data/${this.YangNode._path}`;
					break;
				case 'rpc':
					restStmt = `POST ${ReferenceComponent.PREAMBLE}/restconf/operations/${this.YangNode._path}`;
					break;
				default:
					return;
			}
			restStmt += '\n';
			restStmt += this.xapiHeader;
			restStmt += 'Content-Type: application/json\n\n';
			let payload: any = {};
			let payloadIds = [];
			this.buildJson(this.findNode('input'), payload, payloadIds);
			this.processInnerHtml(this._operationCode, restStmt, payload, payloadIds);
		}
	}
	private get xapiHeader(): string {
		if (this._currentDocNode && this._currentDocNode.data._keyword == 'module') {
			return '';
		} else {
			return `X-Api-Key: "api-key returned from the authenticate rpc"\n`;
		}
	}

	private findNode(name: string): any {
		return this._currentDocNode.data.children.find((c) => c.name == name);
	}
	private buildJson(dataNode: any, payload: any, payloadIds: Array<number>): any {
		if (dataNode) {
			switch (dataNode._keyword) {
				case 'input':
				case 'output':
				case 'container':
					let name = `oht:${dataNode.name}`;
					if (payloadIds && Object.keys(payload).length === 0) {
						name = `oht:${this.makeHyperLink(dataNode)}`;
						payloadIds.push(dataNode.id);
					}
					payload[name] = {}
					if (dataNode.children) {
						for (let childNode of dataNode.children) {
							this.buildJson(childNode, payload[name], payloadIds);
						}
					}
					break;
				default:
					if (payloadIds) {
						payload[this.makeHyperLink(dataNode)] = `${dataNode._type}`;
						payloadIds.push(dataNode.id);
					} else {
						payload[dataNode.name] = dataNode._type;
					}
					break;
			}
		}
		return payload;
	}
	private processInnerHtml(elementRef: ElementRef, restStmt: string, payload: any, payloadIds: Array<number>) {
		if (payloadIds.length > 0) {
			elementRef.nativeElement.innerHTML = restStmt + JSON.stringify(payload, null, 4);
			for (let payloadId of payloadIds) {
				let payloadElement: HTMLElement = elementRef.nativeElement.querySelector('#node' + payloadId);
				payloadElement.style.color = 'blue';
				payloadElement.style.cursor = 'pointer';
				payloadElement.addEventListener("click", () => { this.gotoNode(payloadId); });
			}
		} else {
			elementRef.nativeElement.innerHTML = restStmt;
		}
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
	private isMethod(yangNode: IYangNode): boolean {
		if (yangNode) {
			switch(yangNode._keyword) {
				case 'rpc':
				case 'action':
					return true;
				default:
					return false;
			}
		}
		return false;
	}
	private isProperty(yangNode: IYangNode): boolean {
		switch(yangNode._keyword) {
			case 'leaf':
			case 'leaf-list':
				return true;
			default:
				return false;
		}
	}
	private isList(yangNode: IYangNode): boolean {
		if (yangNode)
			return yangNode._keyword === 'list';
		return false;
	}
	private isLeafRef(yangNode: IYangNode): boolean {
		if (yangNode) {
			return this.isProperty(yangNode) && yangNode._type.search(/(leafref|union[leafref])/g) !== -1;
		}
		return false;	
	}
	private addAccessorCode(code: string[], leftSideName: string) {
		let accessorComment: boolean = false;
			if (this.YangNode.children) {
			for (let childNode of this.YangNode.children) {
				if(this.isProperty(childNode)) {
					if (!accessorComment) {
						code.push(`# access the values of leaf and leaf-list nodes using properties\n`);
						accessorComment = true;
					}
					code.push(`print(${leftSideName}.${this.pythonName(childNode.name)})\n`);
				}
			}
		}
		if (accessorComment) {
			code.push(`\n`);
		}
	}
	private getPropertyEqualsValue(yangNode: IYangNode, parentNode: IYangNode = undefined): string {
		let value = `None`;
		if (parentNode && parentNode._key === yangNode.name) {
			value = `'A unique ${parentNode.name} ${yangNode.name} ${this.nextId}'`;
		} else if (this.isLeafRef(yangNode) && this.getNodePathFromLeafRefPath(yangNode) !== parentNode._path) {
			value = parentNode.name.toLowerCase().replace(/-/g, '_') + '_' + yangNode.name.toLowerCase().replace(/-/g, '_');
		} 
		else if (yangNode._type_pattern) {
			value = `'${yangNode._type_pattern}'`;
		}
		let hyperlink = this.createHyperlink(yangNode.id, this.pythonName(yangNode.name));	
		return `${hyperlink}=${value}`;
	}
	private getNode(currentNode: TreeNode, yangPath: string): TreeNode {
		if (currentNode.data._path === yangPath) {
			return currentNode;
		}
		if (currentNode.children) {
			for (let child of currentNode.children) {
				let match = this.getNode(child, yangPath);
				if (match) {
					return match;
				}
			}
		}
		return undefined;
	}
	private getOptionalParameters(yangNode: IYangNode): string[] {
		let optional_parameters = [];
		if (yangNode.children) {
			for (let child of yangNode.children) {
				if (child.name === yangNode._key || child._writeable === false) {
					continue;
				}
				if(this.isProperty(child)) {
					optional_parameters.push(`, ${this.getPropertyEqualsValue(child, yangNode)}`);
				}
			}
		}
		return optional_parameters;		
	}
	private getNodePathFromLeafRefPath(yangNode: IYangNode): string {
		for (let leafRefPath of yangNode._leafref_paths) {
			let pieces = `oht:${leafRefPath.substr(1)}`.split('/');
			pieces.pop();
			let nodePath = pieces.join('/');
			if (yangNode._path !== nodePath) {
				return nodePath;
			}
		}
		return undefined;
	}
	private setPythonSample() {
		if (this._sampleCode === undefined)
			return;

		let code = [];
		if (this.isMethod(this.YangNode)) {
			code.push(`# The following is a sample that demonstrates how to build a configuration in order to call the ${this.YangNode.name} method\n\n`)
		} else {
			code.push(`# The following is a sample that demonstrates how to build a configuration in order to access the ${this.pythonName(this.YangNode.name)} class\n\n`)
		}
		code.push(`from openhltest_client.httptransport import HttpTransport\n\n`)
		code.push(`# create an instance of the transport class\n`);
		code.push('# by default the HttpTransport will use the internal MockServer to allow for baseline testing\n')
		code.push('# to connect to a vendor server implementation pass in a valid hostname or ip address\n')
		code.push(`vendors_openhltest_server = None\n`);
		code.push(`transport = HttpTransport(vendors_openhltest_server, api_key='optional api key')\n\n`);
		code.push(`# get an instance of the OpenHlTest module class\n`);
		code.push('openhltest = transport.OpenHlTest\n\n');

		let treeNodePath = [];
		let leafRefNodes = Array<ILeafRefNode>();
		let currentNode = this._currentDocNode;
		while (currentNode && currentNode.data._keyword != 'module') {
			if (currentNode.children) {
				for (let child of currentNode.children) {
					if (this.isLeafRef(child.data)) {
						let nodePath = this.getNodePathFromLeafRefPath(child.data);
						if (nodePath) {
							let leafRefNode = this.getNode(this.rootNode, nodePath);
							if (leafRefNode.data._path !== currentNode.data._path) {
								leafRefNodes.push({sourceNode: child, targetNode: leafRefNode});
							}
						}
					}
				}
			}	

			switch(currentNode.data._keyword) {
				case 'list':
				case 'container':
					treeNodePath.unshift(currentNode);
					break;
			}
			currentNode = currentNode.parent;
		}

		// insert leaf ref nodes 
		for (let leafRefNode of leafRefNodes) {
			let pieces = leafRefNode.targetNode.data._path.split('/');
			pieces.pop();
			let parentPath = pieces.join('/');
			let index = treeNodePath.findIndex((p) => p.data._path === parentPath);
			if (index !== -1) {
				treeNodePath.splice(index + 1, 0, leafRefNode);
			}
		}

		let leftSideName: string = 'openhltest';
		for (let treeNode of treeNodePath) {
			let isTreeNode = true;
			if ((<ILeafRefNode>treeNode).sourceNode) {
				let sourceNode = (<ILeafRefNode>treeNode).sourceNode;
				leftSideName = sourceNode.parent.data.name.toLowerCase().replace(/-/g, '_') + '_' + sourceNode.data.name.toLowerCase().replace(/-/g, '_');
				treeNode = (<ILeafRefNode>treeNode).targetNode;
				isTreeNode = false;
			} else {
				leftSideName = treeNode.data.name.toLowerCase().replace(/-/g, '_');
			}
			let action = treeNode.data._keyword === 'list' ? 'create' : 'get';
			code.push(`# ${action} an instance of the ${this.pythonName(treeNode.data.name)} class\n`);
			//code.push(`# except for the ${this.pythonName(treeNode.data.name)} parameter, all of the remaining parameters in the create method are optional\n`);
			let rightSideName = treeNode.parent.data.name.toLowerCase().replace(/-/g, '_');
			code.push(`${leftSideName} = ${rightSideName}.${this.pythonName(treeNode.data.name)}`);

			let optional_parameters = this.getOptionalParameters(treeNode.data);

			if (action === 'create') {
				let keyNode = treeNode.data.children.find((c) => c.name == treeNode.data._key);
				code.push(`.create(${this.getPropertyEqualsValue(keyNode, treeNode.data)}`);
				if (optional_parameters.length > 0) {
					code.push(optional_parameters.join(''));
				}
				code.push(`)\n\n`);
			} else {
				code.push(`\n\n`);				
			}

			if (!isTreeNode) {
				continue;
			}
			
			if (optional_parameters.length > 0 && treeNode.data.name === this.YangNode.name) {
				code.push(`# update the current ${this.pythonName(treeNode.data.name)} resource encapsulated in the ${leftSideName} instance\n`);
				code.push(`# all of the parameters in the update method are optional\n`);
				code.push(`${leftSideName}.update(`);
				code.push(`${optional_parameters.join('').substr(1).trim()})\n\n`);
			}
			
			if (treeNode.data.name === this.YangNode.name) {
				this.addAccessorCode(code, leftSideName);
			}

			if (action === 'create' && treeNode.data.name === this.YangNode.name) {
				code.push(`# delete the current ${this.pythonName(treeNode.data.name)} resource(s) encapsulated in the ${leftSideName} instance\n`);
				code.push(`${leftSideName}.delete()\n\n`);
			}
		}

		if(this.isMethod(this.YangNode)) {
			let input = undefined;
			let output = undefined;
			for (let io of this.YangNode.children) {
				switch (io.name) {
					case 'input':
						input = {};
						this.buildJson(io, input, null);
						break;
					case 'output':
						output = {};
						this.buildJson(io, output, null);
						break;
				}
			}
			code.push(`''' call the ${this.pythonName(this.YangNode.name)} method\n`);
			code.push(`${this.YangNode._description.replace(/\n\t/g, '').trim()}\n`);
			if (output) {
				code.push(`\n`);
				code.push(`the output of the ${this.YangNode._keyword} will have the following structure:\n`);
				for (let line of JSON.stringify(output, null, 4).split('\n')) {
					code.push(`${line}\n`);
				}
			}
			code.push(`'''\n`);
			if (input) {
				code.push(`input = ${JSON.stringify(input, null, 4)}\n`);
				code.push(`output = ${leftSideName}.${this.pythonName(this.YangNode.name)}(input)\n\n`);
			} else {
				code.push(`output = ${leftSideName}.${this.pythonName(this.YangNode.name)}()\n\n`);
			}
		}

		this._sampleCode.nativeElement.innerHTML = code.join('');
		this.processElementRef(this._sampleCode);
	}

	private processElementRef(elementRef: ElementRef) {
		for(let span of elementRef.nativeElement.querySelectorAll('span')) {
			if (span.id.indexOf('node') == 0) {
				let nodeId = span.id.split('node')[1];
				span.style.color = 'blue';
				span.style.cursor = 'pointer';
				span.addEventListener("click", () => { this.gotoNode(nodeId); });
			}
		}		
	}
}
