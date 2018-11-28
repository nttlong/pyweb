angularDefine(function(mdl){

    mdl.directive("select2",["$parse",function($parse){
        return {
            restrict:"ECA",
            template:"<select style=\"width:100%\"></select>",
            replace:true,
            link:function(s,e,a){

                var config={
                    data:s.$eval(a.source)||[],
                    placeholder: a.placeholder,
                    allowClear: true
                }
                var isManulaChange=false;
                var instance=$(e[0]).select2(config).data("select2");
                instance.$element.on("select2:select",function(evt){
                    isManulaChange=true;
                    if(a.ngModel){
                        $parse(a.ngModel).assign(s,$(evt.currentTarget).val());
                    }
                    if(a.ngChange){
                        var fn=s.$eval(a.ngChange);
                        if(angular.isFunction(fn)){
                            fn(v);
                        }
                    }
                    s.$applyAsync();
                    isManulaChange=false;
                })
                a.$observe("placeholder",function(v){
                    config.placeholder=v;
                    instance.$element.select2(config);
                });
                s.$watch(a.ngModel,function(v,o){
                    if(isManulaChange) return;
                    if(v!=o){
                        instance.val(v).trigger("change");
                        
                    }
                });
                s.$watch(a.source,function(v,o){
                    if(o!==v){
                        //$(e[0]).select2("destroy");
                            config.data=v;
                            instance.$element.select2(config);
                            //instance=$(e[0]).select2(config).data("select2");
                            //instance.setData(v);
                    }
                })
                
            }
        }
    }]);
})