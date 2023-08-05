(window.webpackJsonp=window.webpackJsonp||[]).push([[61],{1852:function(e,n,t){"use strict";t.r(n);var r,i,o,a,u,s,c,f,d,l,g,h,m,p,v,b=monaco.Promise,k=function(){function e(e){var n=this;this._defaults=e,this._worker=null,this._idleCheckInterval=setInterval(function(){return n._checkIfIdle()},3e4),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange(function(){return n._stopWorker()})}return e.prototype._stopWorker=function(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null},e.prototype.dispose=function(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()},e.prototype._checkIfIdle=function(){this._worker&&(Date.now()-this._lastUsedTime>12e4&&this._stopWorker())},e.prototype._getClient=function(){return this._lastUsedTime=Date.now(),this._client||(this._worker=monaco.editor.createWebWorker({moduleId:"vs/language/json/jsonWorker",label:this._defaults.languageId,createData:{languageSettings:this._defaults.diagnosticsOptions,languageId:this._defaults.languageId}}),this._client=this._worker.getProxy()),this._client},e.prototype.getLanguageServiceWorker=function(){for(var e,n=this,t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];return function(e){var n,t,r=new b(function(e,r){n=e,t=r},function(){});return e.then(n,t),r}(this._getClient().then(function(n){e=n}).then(function(e){return n._worker.withSyncedResources(t)}).then(function(n){return e}))},e}();!function(e){e.create=function(e,n){return{line:e,character:n}},e.is=function(e){var n=e;return J.objectLiteral(n)&&J.number(n.line)&&J.number(n.character)}}(r||(r={})),function(e){e.create=function(e,n,t,i){if(J.number(e)&&J.number(n)&&J.number(t)&&J.number(i))return{start:r.create(e,n),end:r.create(t,i)};if(r.is(e)&&r.is(n))return{start:e,end:n};throw new Error("Range#create called with invalid arguments["+e+", "+n+", "+t+", "+i+"]")},e.is=function(e){var n=e;return J.objectLiteral(n)&&r.is(n.start)&&r.is(n.end)}}(i||(i={})),function(e){e.create=function(e,n){return{uri:e,range:n}},e.is=function(e){var n=e;return J.defined(n)&&i.is(n.range)&&(J.string(n.uri)||J.undefined(n.uri))}}(o||(o={})),function(e){e.create=function(e,n,t,r){return{red:e,green:n,blue:t,alpha:r}},e.is=function(e){var n=e;return J.number(n.red)&&J.number(n.green)&&J.number(n.blue)&&J.number(n.alpha)}}(a||(a={})),function(e){e.create=function(e,n){return{range:e,color:n}},e.is=function(e){var n=e;return i.is(n.range)&&a.is(n.color)}}(u||(u={})),function(e){e.create=function(e,n,t){return{label:e,textEdit:n,additionalTextEdits:t}},e.is=function(e){var n=e;return J.string(n.label)&&(J.undefined(n.textEdit)||m.is(n))&&(J.undefined(n.additionalTextEdits)||J.typedArray(n.additionalTextEdits,m.is))}}(s||(s={})),function(e){e.Comment="comment",e.Imports="imports",e.Region="region"}(c||(c={})),function(e){e.create=function(e,n,t,r,i){var o={startLine:e,endLine:n};return J.defined(t)&&(o.startCharacter=t),J.defined(r)&&(o.endCharacter=r),J.defined(i)&&(o.kind=i),o},e.is=function(e){var n=e;return J.number(n.startLine)&&J.number(n.startLine)&&(J.undefined(n.startCharacter)||J.number(n.startCharacter))&&(J.undefined(n.endCharacter)||J.number(n.endCharacter))&&(J.undefined(n.kind)||J.string(n.kind))}}(f||(f={})),function(e){e.create=function(e,n){return{location:e,message:n}},e.is=function(e){var n=e;return J.defined(n)&&o.is(n.location)&&J.string(n.message)}}(d||(d={})),function(e){e.Error=1,e.Warning=2,e.Information=3,e.Hint=4}(l||(l={})),function(e){e.create=function(e,n,t,r,i,o){var a={range:e,message:n};return J.defined(t)&&(a.severity=t),J.defined(r)&&(a.code=r),J.defined(i)&&(a.source=i),J.defined(o)&&(a.relatedInformation=o),a},e.is=function(e){var n=e;return J.defined(n)&&i.is(n.range)&&J.string(n.message)&&(J.number(n.severity)||J.undefined(n.severity))&&(J.number(n.code)||J.string(n.code)||J.undefined(n.code))&&(J.string(n.source)||J.undefined(n.source))&&(J.undefined(n.relatedInformation)||J.typedArray(n.relatedInformation,d.is))}}(g||(g={})),function(e){e.create=function(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={title:e,command:n};return J.defined(t)&&t.length>0&&(i.arguments=t),i},e.is=function(e){var n=e;return J.defined(n)&&J.string(n.title)&&J.string(n.command)}}(h||(h={})),function(e){e.replace=function(e,n){return{range:e,newText:n}},e.insert=function(e,n){return{range:{start:e,end:e},newText:n}},e.del=function(e){return{range:e,newText:""}},e.is=function(e){var n=e;return J.objectLiteral(n)&&J.string(n.newText)&&i.is(n.range)}}(m||(m={})),function(e){e.create=function(e,n){return{textDocument:e,edits:n}},e.is=function(e){var n=e;return J.defined(n)&&C.is(n.textDocument)&&Array.isArray(n.edits)}}(p||(p={})),function(e){e.is=function(e){var n=e;return n&&(void 0!==n.changes||void 0!==n.documentChanges)&&(void 0===n.documentChanges||J.typedArray(n.documentChanges,p.is))}}(v||(v={}));var y,C,_,w,x,E,S,I,A,T,M,P,j,F,L,O,R,D=function(){function e(e){this.edits=e}return e.prototype.insert=function(e,n){this.edits.push(m.insert(e,n))},e.prototype.replace=function(e,n){this.edits.push(m.replace(e,n))},e.prototype.delete=function(e){this.edits.push(m.del(e))},e.prototype.add=function(e){this.edits.push(e)},e.prototype.all=function(){return this.edits},e.prototype.clear=function(){this.edits.splice(0,this.edits.length)},e}();!function(){function e(e){var n=this;this._textEditChanges=Object.create(null),e&&(this._workspaceEdit=e,e.documentChanges?e.documentChanges.forEach(function(e){var t=new D(e.edits);n._textEditChanges[e.textDocument.uri]=t}):e.changes&&Object.keys(e.changes).forEach(function(t){var r=new D(e.changes[t]);n._textEditChanges[t]=r}))}Object.defineProperty(e.prototype,"edit",{get:function(){return this._workspaceEdit},enumerable:!0,configurable:!0}),e.prototype.getTextEditChange=function(e){if(C.is(e)){if(this._workspaceEdit||(this._workspaceEdit={documentChanges:[]}),!this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for versioned document changes.");var n=e;if(!(r=this._textEditChanges[n.uri])){var t={textDocument:n,edits:i=[]};this._workspaceEdit.documentChanges.push(t),r=new D(i),this._textEditChanges[n.uri]=r}return r}if(this._workspaceEdit||(this._workspaceEdit={changes:Object.create(null)}),!this._workspaceEdit.changes)throw new Error("Workspace edit is not configured for normal text edit changes.");var r;if(!(r=this._textEditChanges[e])){var i=[];this._workspaceEdit.changes[e]=i,r=new D(i),this._textEditChanges[e]=r}return r}}();!function(e){e.create=function(e){return{uri:e}},e.is=function(e){var n=e;return J.defined(n)&&J.string(n.uri)}}(y||(y={})),function(e){e.create=function(e,n){return{uri:e,version:n}},e.is=function(e){var n=e;return J.defined(n)&&J.string(n.uri)&&J.number(n.version)}}(C||(C={})),function(e){e.create=function(e,n,t,r){return{uri:e,languageId:n,version:t,text:r}},e.is=function(e){var n=e;return J.defined(n)&&J.string(n.uri)&&J.string(n.languageId)&&J.number(n.version)&&J.string(n.text)}}(_||(_={})),function(e){e.PlainText="plaintext",e.Markdown="markdown"}(w||(w={})),function(e){e.is=function(n){var t=n;return t===e.PlainText||t===e.Markdown}}(w||(w={})),function(e){e.is=function(e){var n=e;return J.objectLiteral(e)&&w.is(n.kind)&&J.string(n.value)}}(x||(x={})),function(e){e.Text=1,e.Method=2,e.Function=3,e.Constructor=4,e.Field=5,e.Variable=6,e.Class=7,e.Interface=8,e.Module=9,e.Property=10,e.Unit=11,e.Value=12,e.Enum=13,e.Keyword=14,e.Snippet=15,e.Color=16,e.File=17,e.Reference=18,e.Folder=19,e.EnumMember=20,e.Constant=21,e.Struct=22,e.Event=23,e.Operator=24,e.TypeParameter=25}(E||(E={})),function(e){e.PlainText=1,e.Snippet=2}(S||(S={})),function(e){e.create=function(e){return{label:e}}}(I||(I={})),function(e){e.create=function(e,n){return{items:e||[],isIncomplete:!!n}}}(A||(A={})),function(e){e.fromPlainText=function(e){return e.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")},e.is=function(e){var n=e;return J.string(n)||J.objectLiteral(n)&&J.string(n.language)&&J.string(n.value)}}(T||(T={})),function(e){e.is=function(e){var n=e;return J.objectLiteral(n)&&(x.is(n.contents)||T.is(n.contents)||J.typedArray(n.contents,T.is))&&(void 0===e.range||i.is(e.range))}}(M||(M={})),function(e){e.create=function(e,n){return n?{label:e,documentation:n}:{label:e}}}(P||(P={})),function(e){e.create=function(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={label:e};return J.defined(n)&&(i.documentation=n),J.defined(t)?i.parameters=t:i.parameters=[],i}}(j||(j={})),function(e){e.Text=1,e.Read=2,e.Write=3}(F||(F={})),function(e){e.create=function(e,n){var t={range:e};return J.number(n)&&(t.kind=n),t}}(L||(L={})),function(e){e.File=1,e.Module=2,e.Namespace=3,e.Package=4,e.Class=5,e.Method=6,e.Property=7,e.Field=8,e.Constructor=9,e.Enum=10,e.Interface=11,e.Function=12,e.Variable=13,e.Constant=14,e.String=15,e.Number=16,e.Boolean=17,e.Array=18,e.Object=19,e.Key=20,e.Null=21,e.EnumMember=22,e.Struct=23,e.Event=24,e.Operator=25,e.TypeParameter=26}(O||(O={})),function(e){e.create=function(e,n,t,r,i){var o={name:e,kind:n,location:{uri:r,range:t}};return i&&(o.containerName=i),o}}(R||(R={}));var W,N,V,K,U,z=function(){return function(){}}();!function(e){e.create=function(e,n,t,r,i,o){var a={name:e,detail:n,kind:t,range:r,selectionRange:i};return void 0!==o&&(a.children=o),a},e.is=function(e){var n=e;return n&&J.string(n.name)&&J.string(n.detail)&&J.number(n.kind)&&i.is(n.range)&&i.is(n.selectionRange)&&(void 0===n.deprecated||J.boolean(n.deprecated))&&(void 0===n.children||Array.isArray(n.children))}}(z||(z={})),function(e){e.QuickFix="quickfix",e.Refactor="refactor",e.RefactorExtract="refactor.extract",e.RefactorInline="refactor.inline",e.RefactorRewrite="refactor.rewrite",e.Source="source",e.SourceOrganizeImports="source.organizeImports"}(W||(W={})),function(e){e.create=function(e,n){var t={diagnostics:e};return void 0!==n&&null!==n&&(t.only=n),t},e.is=function(e){var n=e;return J.defined(n)&&J.typedArray(n.diagnostics,g.is)&&(void 0===n.only||J.typedArray(n.only,J.string))}}(N||(N={})),function(e){e.create=function(e,n,t){var r={title:e};return h.is(n)?r.command=n:r.edit=n,void 0!==t&&(r.kind=t),r},e.is=function(e){var n=e;return n&&J.string(n.title)&&(void 0===n.diagnostics||J.typedArray(n.diagnostics,g.is))&&(void 0===n.kind||J.string(n.kind))&&(void 0!==n.edit||void 0!==n.command)&&(void 0===n.command||h.is(n.command))&&(void 0===n.edit||v.is(n.edit))}}(V||(V={})),function(e){e.create=function(e,n){var t={range:e};return J.defined(n)&&(t.data=n),t},e.is=function(e){var n=e;return J.defined(n)&&i.is(n.range)&&(J.undefined(n.command)||h.is(n.command))}}(K||(K={})),function(e){e.create=function(e,n){return{tabSize:e,insertSpaces:n}},e.is=function(e){var n=e;return J.defined(n)&&J.number(n.tabSize)&&J.boolean(n.insertSpaces)}}(U||(U={}));var H=function(){return function(){}}();!function(e){e.create=function(e,n,t){return{range:e,target:n,data:t}},e.is=function(e){var n=e;return J.defined(n)&&i.is(n.range)&&(J.undefined(n.target)||J.string(n.target))}}(H||(H={}));var q,B;!function(e){e.create=function(e,n,t,r){return new $(e,n,t,r)},e.is=function(e){var n=e;return!!(J.defined(n)&&J.string(n.uri)&&(J.undefined(n.languageId)||J.string(n.languageId))&&J.number(n.lineCount)&&J.func(n.getText)&&J.func(n.positionAt)&&J.func(n.offsetAt))},e.applyEdits=function(e,n){for(var t=e.getText(),r=function e(n,t){if(n.length<=1)return n;var r=n.length/2|0,i=n.slice(0,r),o=n.slice(r);e(i,t),e(o,t);for(var a=0,u=0,s=0;a<i.length&&u<o.length;){var c=t(i[a],o[u]);n[s++]=c<=0?i[a++]:o[u++]}for(;a<i.length;)n[s++]=i[a++];for(;u<o.length;)n[s++]=o[u++];return n}(n,function(e,n){var t=e.range.start.line-n.range.start.line;return 0===t?e.range.start.character-n.range.start.character:t}),i=t.length,o=r.length-1;o>=0;o--){var a=r[o],u=e.offsetAt(a.range.start),s=e.offsetAt(a.range.end);if(!(s<=i))throw new Error("Ovelapping edit");t=t.substring(0,u)+a.newText+t.substring(s,t.length),i=u}return t}}(q||(q={})),function(e){e.Manual=1,e.AfterDelay=2,e.FocusOut=3}(B||(B={}));var J,$=function(){function e(e,n,t,r){this._uri=e,this._languageId=n,this._version=t,this._content=r,this._lineOffsets=null}return Object.defineProperty(e.prototype,"uri",{get:function(){return this._uri},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"languageId",{get:function(){return this._languageId},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"version",{get:function(){return this._version},enumerable:!0,configurable:!0}),e.prototype.getText=function(e){if(e){var n=this.offsetAt(e.start),t=this.offsetAt(e.end);return this._content.substring(n,t)}return this._content},e.prototype.update=function(e,n){this._content=e.text,this._version=n,this._lineOffsets=null},e.prototype.getLineOffsets=function(){if(null===this._lineOffsets){for(var e=[],n=this._content,t=!0,r=0;r<n.length;r++){t&&(e.push(r),t=!1);var i=n.charAt(r);t="\r"===i||"\n"===i,"\r"===i&&r+1<n.length&&"\n"===n.charAt(r+1)&&r++}t&&n.length>0&&e.push(n.length),this._lineOffsets=e}return this._lineOffsets},e.prototype.positionAt=function(e){e=Math.max(Math.min(e,this._content.length),0);var n=this.getLineOffsets(),t=0,i=n.length;if(0===i)return r.create(0,e);for(;t<i;){var o=Math.floor((t+i)/2);n[o]>e?i=o:t=o+1}var a=t-1;return r.create(a,e-n[a])},e.prototype.offsetAt=function(e){var n=this.getLineOffsets();if(e.line>=n.length)return this._content.length;if(e.line<0)return 0;var t=n[e.line],r=e.line+1<n.length?n[e.line+1]:this._content.length;return Math.max(Math.min(t+e.character,r),t)},Object.defineProperty(e.prototype,"lineCount",{get:function(){return this.getLineOffsets().length},enumerable:!0,configurable:!0}),e}();!function(e){var n=Object.prototype.toString;e.defined=function(e){return void 0!==e},e.undefined=function(e){return void 0===e},e.boolean=function(e){return!0===e||!1===e},e.string=function(e){return"[object String]"===n.call(e)},e.number=function(e){return"[object Number]"===n.call(e)},e.func=function(e){return"[object Function]"===n.call(e)},e.objectLiteral=function(e){return null!==e&&"object"==typeof e},e.typedArray=function(e,n){return Array.isArray(e)&&e.every(n)}}(J||(J={}));monaco.Uri;var Q=monaco.Range,G=function(){function e(e,n,t){var r=this;this._languageId=e,this._worker=n,this._disposables=[],this._listener=Object.create(null);var i=function(e){var n,t=e.getModeId();t===r._languageId&&(r._listener[e.uri.toString()]=e.onDidChangeContent(function(){clearTimeout(n),n=setTimeout(function(){return r._doValidate(e.uri,t)},500)}),r._doValidate(e.uri,t))},o=function(e){monaco.editor.setModelMarkers(e,r._languageId,[]);var n=e.uri.toString(),t=r._listener[n];t&&(t.dispose(),delete r._listener[n])};this._disposables.push(monaco.editor.onDidCreateModel(i)),this._disposables.push(monaco.editor.onWillDisposeModel(function(e){o(e),r._resetSchema(e.uri)})),this._disposables.push(monaco.editor.onDidChangeModelLanguage(function(e){o(e.model),i(e.model),r._resetSchema(e.model.uri)})),this._disposables.push(t.onDidChange(function(e){monaco.editor.getModels().forEach(function(e){e.getModeId()===r._languageId&&(o(e),i(e))})})),this._disposables.push({dispose:function(){for(var e in monaco.editor.getModels().forEach(o),r._listener)r._listener[e].dispose()}}),monaco.editor.getModels().forEach(i)}return e.prototype.dispose=function(){this._disposables.forEach(function(e){return e&&e.dispose()}),this._disposables=[]},e.prototype._resetSchema=function(e){this._worker().then(function(n){n.resetSchema(e.toString())})},e.prototype._doValidate=function(e,n){this._worker(e).then(function(t){return t.doValidation(e.toString()).then(function(t){var r=t.map(function(e){return function(e,n){var t="number"==typeof n.code?String(n.code):n.code;return{severity:function(e){switch(e){case l.Error:return monaco.MarkerSeverity.Error;case l.Warning:return monaco.MarkerSeverity.Warning;case l.Information:return monaco.MarkerSeverity.Info;case l.Hint:return monaco.MarkerSeverity.Hint;default:return monaco.MarkerSeverity.Info}}(n.severity),startLineNumber:n.range.start.line+1,startColumn:n.range.start.character+1,endLineNumber:n.range.end.line+1,endColumn:n.range.end.character+1,message:n.message,code:t,source:n.source}}(0,e)}),i=monaco.editor.getModel(e);i.getModeId()===n&&monaco.editor.setModelMarkers(i,n,r)})}).then(void 0,function(e){console.error(e)})},e}();function X(e){if(e)return{character:e.column-1,line:e.lineNumber-1}}function Y(e){if(e)return{start:{line:e.startLineNumber-1,character:e.startColumn-1},end:{line:e.endLineNumber-1,character:e.endColumn-1}}}function Z(e){if(e)return new Q(e.start.line+1,e.start.character+1,e.end.line+1,e.end.character+1)}function ee(e){var n=monaco.languages.CompletionItemKind;switch(e){case E.Text:return n.Text;case E.Method:return n.Method;case E.Function:return n.Function;case E.Constructor:return n.Constructor;case E.Field:return n.Field;case E.Variable:return n.Variable;case E.Class:return n.Class;case E.Interface:return n.Interface;case E.Module:return n.Module;case E.Property:return n.Property;case E.Unit:return n.Unit;case E.Value:return n.Value;case E.Enum:return n.Enum;case E.Keyword:return n.Keyword;case E.Snippet:return n.Snippet;case E.Color:return n.Color;case E.File:return n.File;case E.Reference:return n.Reference}return n.Property}function ne(e){if(e)return{range:Z(e.range),text:e.newText}}var te=function(){function e(e){this._worker=e}return Object.defineProperty(e.prototype,"triggerCharacters",{get:function(){return[" ",":"]},enumerable:!0,configurable:!0}),e.prototype.provideCompletionItems=function(e,n,t){e.getWordUntilPosition(n);var r=e.uri;return de(t,this._worker(r).then(function(e){return e.doComplete(r.toString(),X(n))}).then(function(e){if(e){var n=e.items.map(function(e){var n={label:e.label,insertText:e.insertText,sortText:e.sortText,filterText:e.filterText,documentation:e.documentation,detail:e.detail,kind:ee(e.kind)};return e.textEdit&&(n.range=Z(e.textEdit.range),n.insertText=e.textEdit.newText),e.insertTextFormat===S.Snippet&&(n.insertText={value:n.insertText}),n});return{isIncomplete:e.isIncomplete,items:n}}}))},e}();function re(e){return"string"==typeof e?{value:e}:function(e){return e&&"object"==typeof e&&"string"==typeof e.kind}(e)?"plaintext"===e.kind?{value:e.value.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}:{value:e.value}:{value:"```"+e.language+"\n"+e.value+"\n```\n"}}var ie=function(){function e(e){this._worker=e}return e.prototype.provideHover=function(e,n,t){var r=e.uri;return de(t,this._worker(r).then(function(e){return e.doHover(r.toString(),X(n))}).then(function(e){if(e)return{range:Z(e.range),contents:function(e){if(e)return Array.isArray(e)?e.map(re):[re(e)]}(e.contents)}}))},e}();var oe=function(){function e(e){this._worker=e}return e.prototype.provideDocumentSymbols=function(e,n){var t=e.uri;return de(n,this._worker(t).then(function(e){return e.findDocumentSymbols(t.toString())}).then(function(e){if(e)return e.map(function(e){return{name:e.name,detail:"",containerName:e.containerName,kind:function(e){var n=monaco.languages.SymbolKind;switch(e){case O.File:return n.Array;case O.Module:return n.Module;case O.Namespace:return n.Namespace;case O.Package:return n.Package;case O.Class:return n.Class;case O.Method:return n.Method;case O.Property:return n.Property;case O.Field:return n.Field;case O.Constructor:return n.Constructor;case O.Enum:return n.Enum;case O.Interface:return n.Interface;case O.Function:return n.Function;case O.Variable:return n.Variable;case O.Constant:return n.Constant;case O.String:return n.String;case O.Number:return n.Number;case O.Boolean:return n.Boolean;case O.Array:return n.Array}return n.Function}(e.kind),range:Z(e.location.range),selectionRange:Z(e.location.range)}})}))},e}();function ae(e){return{tabSize:e.tabSize,insertSpaces:e.insertSpaces}}var ue=function(){function e(e){this._worker=e}return e.prototype.provideDocumentFormattingEdits=function(e,n,t){var r=e.uri;return de(t,this._worker(r).then(function(e){return e.format(r.toString(),null,ae(n)).then(function(e){if(e&&0!==e.length)return e.map(ne)})}))},e}(),se=function(){function e(e){this._worker=e}return e.prototype.provideDocumentRangeFormattingEdits=function(e,n,t,r){var i=e.uri;return de(r,this._worker(i).then(function(e){return e.format(i.toString(),Y(n),ae(t)).then(function(e){if(e&&0!==e.length)return e.map(ne)})}))},e}(),ce=function(){function e(e){this._worker=e}return e.prototype.provideDocumentColors=function(e,n){var t=e.uri;return de(n,this._worker(t).then(function(e){return e.findDocumentColors(t.toString())}).then(function(e){if(e)return e.map(function(e){return{color:e.color,range:Z(e.range)}})}))},e.prototype.provideColorPresentations=function(e,n,t){var r=e.uri;return de(t,this._worker(r).then(function(e){return e.getColorPresentations(r.toString(),n.color,Y(n.range))}).then(function(e){if(e)return e.map(function(e){var n={label:e.label};return e.textEdit&&(n.textEdit=ne(e.textEdit)),e.additionalTextEdits&&(n.additionalTextEdits=e.additionalTextEdits.map(ne)),n})}))},e}(),fe=function(){function e(e){this._worker=e}return e.prototype.provideFoldingRanges=function(e,n,t){var r=e.uri;return de(t,this._worker(r).then(function(e){return e.provideFoldingRanges(r.toString(),n)}).then(function(e){if(e)return e.map(function(e){var n={start:e.startLine+1,end:e.endLine+1};return void 0!==e.kind&&(n.kind=function(e){switch(e){case c.Comment:return monaco.languages.FoldingRangeKind.Comment;case c.Imports:return monaco.languages.FoldingRangeKind.Imports;case c.Region:return monaco.languages.FoldingRangeKind.Region}return}(e.kind)),n})}))},e}();function de(e,n){return n.cancel&&e.onCancellationRequested(function(){return n.cancel()}),n}function le(e,n){void 0===n&&(n=!1);var t=0,r=e.length,i="",o=0,a=16,u=0;function s(n,r){for(var i=0,o=0;i<n||!r;){var a=e.charCodeAt(t);if(a>=48&&a<=57)o=16*o+a-48;else if(a>=65&&a<=70)o=16*o+a-65+10;else{if(!(a>=97&&a<=102))break;o=16*o+a-97+10}t++,i++}return i<n&&(o=-1),o}function c(){if(i="",u=0,o=t,t>=r)return o=r,a=17;var n=e.charCodeAt(t);if(ge(n)){do{t++,i+=String.fromCharCode(n),n=e.charCodeAt(t)}while(ge(n));return a=15}if(he(n))return t++,i+=String.fromCharCode(n),13===n&&10===e.charCodeAt(t)&&(t++,i+="\n"),a=14;switch(n){case 123:return t++,a=1;case 125:return t++,a=2;case 91:return t++,a=3;case 93:return t++,a=4;case 58:return t++,a=6;case 44:return t++,a=5;case 34:return t++,i=function(){for(var n="",i=t;;){if(t>=r){n+=e.substring(i,t),u=2;break}var o=e.charCodeAt(t);if(34===o){n+=e.substring(i,t),t++;break}if(92!==o){if(o>=0&&o<=31){if(he(o)){n+=e.substring(i,t),u=2;break}u=6}t++}else{if(n+=e.substring(i,t),++t>=r){u=2;break}switch(o=e.charCodeAt(t++)){case 34:n+='"';break;case 92:n+="\\";break;case 47:n+="/";break;case 98:n+="\b";break;case 102:n+="\f";break;case 110:n+="\n";break;case 114:n+="\r";break;case 116:n+="\t";break;case 117:var a=s(4,!0);a>=0?n+=String.fromCharCode(a):u=4;break;default:u=5}i=t}}return n}(),a=10;case 47:var c=t-1;if(47===e.charCodeAt(t+1)){for(t+=2;t<r&&!he(e.charCodeAt(t));)t++;return i=e.substring(c,t),a=12}if(42===e.charCodeAt(t+1)){t+=2;for(var d=!1;t<r;){if(42===e.charCodeAt(t)&&t+1<r&&47===e.charCodeAt(t+1)){t+=2,d=!0;break}t++}return d||(t++,u=1),i=e.substring(c,t),a=13}return i+=String.fromCharCode(n),t++,a=16;case 45:if(i+=String.fromCharCode(n),++t===r||!me(e.charCodeAt(t)))return a=16;case 48:case 49:case 50:case 51:case 52:case 53:case 54:case 55:case 56:case 57:return i+=function(){var n=t;if(48===e.charCodeAt(t))t++;else for(t++;t<e.length&&me(e.charCodeAt(t));)t++;if(t<e.length&&46===e.charCodeAt(t)){if(!(++t<e.length&&me(e.charCodeAt(t))))return u=3,e.substring(n,t);for(t++;t<e.length&&me(e.charCodeAt(t));)t++}var r=t;if(t<e.length&&(69===e.charCodeAt(t)||101===e.charCodeAt(t)))if((++t<e.length&&43===e.charCodeAt(t)||45===e.charCodeAt(t))&&t++,t<e.length&&me(e.charCodeAt(t))){for(t++;t<e.length&&me(e.charCodeAt(t));)t++;r=t}else u=3;return e.substring(n,r)}(),a=11;default:for(;t<r&&f(n);)t++,n=e.charCodeAt(t);if(o!==t){switch(i=e.substring(o,t)){case"true":return a=8;case"false":return a=9;case"null":return a=7}return a=16}return i+=String.fromCharCode(n),t++,a=16}}function f(e){if(ge(e)||he(e))return!1;switch(e){case 125:case 93:case 123:case 91:case 34:case 58:case 44:case 47:return!1}return!0}return{setPosition:function(e){t=e,i="",o=0,a=16,u=0},getPosition:function(){return t},scan:n?function(){var e;do{e=c()}while(e>=12&&e<=15);return e}:c,getToken:function(){return a},getTokenValue:function(){return i},getTokenOffset:function(){return o},getTokenLength:function(){return t-o},getTokenError:function(){return u}}}function ge(e){return 32===e||9===e||11===e||12===e||160===e||5760===e||e>=8192&&e<=8203||8239===e||8287===e||12288===e||65279===e}function he(e){return 10===e||13===e||8232===e||8233===e}function me(e){return e>=48&&e<=57}var pe=le;function ve(e){return{getInitialState:function(){return new Te(null,null,!1)},tokenize:function(n,t,r,i){return function(e,n,t,r,i){void 0===r&&(r=0);var o=0,a=!1;switch(t.scanError){case 2:n='"'+n,o=1;break;case 1:n="/*"+n,o=2}var u,s,c=pe(n),f=t.lastWasColon;s={tokens:[],endState:t.clone()};for(;;){var d=r+c.getPosition(),l="";if(17===(u=c.scan()))break;if(d===r+c.getPosition())throw new Error("Scanner did not advance, next 3 characters are: "+n.substr(c.getPosition(),3));switch(a&&(d-=o),a=o>0,u){case 1:case 2:l=be,f=!1;break;case 3:case 4:l=ke,f=!1;break;case 6:l=ye,f=!0;break;case 5:l=Ce,f=!1;break;case 8:case 9:l=_e,f=!1;break;case 7:l=we,f=!1;break;case 10:l=f?xe:Se,f=!1;break;case 11:l=Ee,f=!1}if(e)switch(u){case 12:l=Ae;break;case 13:l=Ie}s.endState=new Te(t.getStateData(),c.getTokenError(),f),s.tokens.push({startIndex:d,scopes:l})}return s}(e,n,t,r)}}}var be="delimiter.bracket.json",ke="delimiter.array.json",ye="delimiter.colon.json",Ce="delimiter.comma.json",_e="keyword.json",we="keyword.json",xe="string.value.json",Ee="number.json",Se="string.key.json",Ie="comment.block.json",Ae="comment.line.json",Te=function(){function e(e,n,t){this._state=e,this.scanError=n,this.lastWasColon=t}return e.prototype.clone=function(){return new e(this._state,this.scanError,this.lastWasColon)},e.prototype.equals=function(n){return n===this||!!(n&&n instanceof e)&&(this.scanError===n.scanError&&this.lastWasColon===n.lastWasColon)},e.prototype.getStateData=function(){return this._state},e.prototype.setStateData=function(e){this._state=e},e}();function Me(e){var n=[],t=new k(e);n.push(t);var r=function(){for(var e=[],n=0;n<arguments.length;n++)e[n]=arguments[n];return t.getLanguageServiceWorker.apply(t,e)},i=e.languageId;n.push(monaco.languages.registerCompletionItemProvider(i,new te(r))),n.push(monaco.languages.registerHoverProvider(i,new ie(r))),n.push(monaco.languages.registerDocumentSymbolProvider(i,new oe(r))),n.push(monaco.languages.registerDocumentFormattingEditProvider(i,new ue(r))),n.push(monaco.languages.registerDocumentRangeFormattingEditProvider(i,new se(r))),n.push(new G(i,r,e)),n.push(monaco.languages.setTokensProvider(i,ve(!0))),n.push(monaco.languages.setLanguageConfiguration(i,Pe)),n.push(monaco.languages.registerColorProvider(i,new ce(r))),n.push(monaco.languages.registerFoldingRangeProvider(i,new fe(r)))}t.d(n,"setupMode",function(){return Me});var Pe={wordPattern:/(-?\d*\.\d\w*)|([^\[\{\]\}\:\"\,\s]+)/g,comments:{lineComment:"//",blockComment:["/*","*/"]},brackets:[["{","}"],["[","]"]],autoClosingPairs:[{open:"{",close:"}",notIn:["string"]},{open:"[",close:"]",notIn:["string"]},{open:'"',close:'"',notIn:["string"]}]}}}]);