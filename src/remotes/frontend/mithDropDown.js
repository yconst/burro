var MythDropDown=function(list)  {
    if(Array.isArray(list))
	this.list=list;
    else
	list=[];
    if (!(this instanceof MythDropDown)) 
	return new MythDropDown(list);
    
    var self=this;
    this.selected={
	name:list[0],
	index:0};
    this.list=list;
};

MythDropDown.prototype.view= function(ctrl) {
        var self = this;
        return m('select', {
                config: function(selectElement, isinit) {
                    if (isinit)
                        return;
		    self.selectElement = selectElement;
		    self.update(self.list);
            },
            onchange: function(e) {
                self.selected.name = e.target.value;
		self.selected.index=e.target.selectedIndex;
		
                }
            },

            this.list.map(function(name, i) {
                return m('option', name);
            }));
    };

MythDropDown.prototype.getSelected=function(){
	return (this.selected);
};

MythDropDown.prototype.update=function(newList){
	
	this.list=newList;
	this.selectElement.selectedIndex=0;
	this.selected.name=newList[0];
	this.selected.index=0;
};

MythDropDown.prototype.sort=function(){
    this.list.sort();
    this.update(this.list);
};

MythDropDown.prototype.delete=function(){
    this.list.splice(this.selected.index,1);
    this.update(this.list);
    
};
