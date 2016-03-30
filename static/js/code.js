var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    parserfile: ["parsepython.js"],
    autofocus: true,
    theme: "solarized dark",
    lineNumbers: true,
    textWrapping: false,
    indentUnit: 4,
    height: "160px",
    fontSize: "9pt",
    autoMatchParens: true,
    parserConfig: {'pythonVersion': 2, 'strictErrors': true}
});

function outf(text) {
    var mypre = document.getElementById("output");
    mypre.innerHTML = mypre.innerHTML + text;
}

function runit() {
   var prog = editor.getValue();
   var mypre = document.getElementById("output");
   mypre.innerHTML = '';
   Sk.pre = "output";
   Sk.configure({output:outf});
   var myPromise = Sk.misceval.asyncToPromise(function() {
       return Sk.importMainWithBody("<stdin>", false, prog, true);
   });
   myPromise.then(function(mod) {
       console.log('success');
   },
       function(err) {
       console.log(err.toString());
   });
}
