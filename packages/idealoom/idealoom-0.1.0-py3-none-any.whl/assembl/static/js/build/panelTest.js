webpackJsonp([2,7],{

/***/ 0:
/*!************************************!*\
  !*** ./js/app/views/testPanels.js ***!
  \************************************/
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	var Backbone = __webpack_require__(/*! backbone */ 3),
	    Marionette = __webpack_require__(/*! backbone.marionette */ 5),
	    _ = __webpack_require__(/*! underscore */ 2),
	    $ = __webpack_require__(/*! jquery */ 1),
	    panels = __webpack_require__(/*! ./panels.js */ 363);
	
	var TestPanel = panels.BasePanel.extend({
	  constructor: function TestPanel() {
	    panels.BasePanel.apply(this, arguments);
	    this.model = new Backbone.Model();
	    if (this.model.get('subpanels') === undefined) {
	      this.model.set('subpanels', []);
	    }
	  },
	
	  ui: {
	    dropdown: '#dropdown',
	  },
	
	  events: {
	    'change @ui.dropdown': 'selectChanged',
	  },
	
	  selectChanged: function(event) {
	    this.model.set('subpanels', _.filter(event.target.value.split('_'), function(x) {
	      return x.length > 0;
	    }));
	    this.wrapper.panelGroup.changeSelection({});
	  },
	
	  getAllowedPanelNames: function() {
	      return this.model.get('subpanels');
	  },
	
	  getAutoactivatedPanelNames: function() {
	      return this.model.get('subpanels');
	  },
	
	  serializeData: function() {
	    return {
	      panelN: this.wrapper.indexInLevel(),
	      levelN: this.wrapper.panelLevel.indexInColumn(),
	      columnN: this.wrapper.panelColumn.indexInColumns(),
	      groupN: this.wrapper.panelGroup.indexInManager(),
	    };
	  },
	
	  name: 'test',
	  className: 'panel test-panel',
	  template: _.template(
	    'G<%= groupN %>C<%= columnN %>L<%= levelN %>P<%= panelN %> '+
	    'choose: <select id="dropdown" name="dropdown">'+
	    '<option id="" selected></option>'+
	    '<option id="test">test</option>'+
	    '<option id="test2">test2</option>'+
	    '<option id="test21">test2_test</option>'+
	    '</select>'),
	});
	
	var Test2Panel = TestPanel.extend({
	  constructor: function Test2Panel() {
	    TestPanel.apply(this, arguments);
	  },
	  name: 'test2',
	  className: 'panel test2-panel',
	});
	
	panels.PanelManager.prototype.registerPanelClass(TestPanel);
	panels.PanelManager.prototype.registerPanelClass(Test2Panel);
	
	
	var App =  Marionette.Application.extend({
	  region: '#testapp',
	
	  onStart: function() {
	    this.panelManager = new panels.PanelManager({
	      rootName: 'test',
	    });
	    this.showView(this.panelManager);
	    this.panelManager.children.each(function(group) {
	      group.changeSelection({});
	    });
	    $(window).on("resize", _.bind(this.windowResized, this));
	  },
	  windowResized: function() {
	    this.panelManager.resize(window.innerWidth);
	  },
	});
	
	document.addEventListener('DOMContentLoaded', () => {
	  var app = new App();
	  window.app = app;
	  app.start();
	});


/***/ },

/***/ 363:
/*!********************************!*\
  !*** ./js/app/views/panels.js ***!
  \********************************/
/***/ function(module, exports, __webpack_require__) {

	'use strict';
	
	// Note on animation: https://github.com/marionettejs/backbone.marionette/issues/320
	// https://github.com/marcinkrysiak1979/marionette.showAnimated/blob/master/backbone.marionette.showAnimated.js
	
	/**
	 *
	 * @module app.views.panels
	 */
	
	var Backbone = __webpack_require__(/*! backbone */ 3),
	    Marionette = __webpack_require__(/*! backbone.marionette */ 5),
	    _ = __webpack_require__(/*! underscore */ 2);
	
	
	function assert(condition, msg) {
	  if (!condition) {
	    console.error(msg || "error");
	    debugger;
	  }
	}
	
	/**
	 * @class app.views.panels.ViewModel
	 */
	var ViewModel = Backbone.Model.extend({
	  constructor: function ViewModel() {
	    Backbone.Model.apply(this, arguments);
	  },
	});
	
	/**
	 * @class app.views.panels.ViewModelCollection
	 */
	var ViewModelCollection = Backbone.Collection.extend({
	  constructor: function ViewModelCollection() {
	    Backbone.Collection.apply(this, arguments);
	  },
	  model: ViewModel,
	});
	
	/**
	 * @class app.views.panels.PanelModel
	 */
	var PanelModel = ViewModel.extend({
	  constructor: function PanelModel() {
	    ViewModel.apply(this, arguments);
	  },
	  defaults: {
	    panelName: '',
	    minimized: false,
	  },
	});
	
	/**
	 * @class app.views.panels.PanelModelCollection
	 */
	var PanelModelCollection = ViewModelCollection.extend({
	  constructor: function PanelModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelModel,
	});
	
	
	/**
	 * @class app.views.panels.PanelLevelModel
	 */
	var PanelLevelModel = ViewModel.extend({
	  constructor: function PanelLevelModel() {
	    ViewModel.apply(this, arguments);
	  },
	  defaults: function() {
	    return {
	      collection: new PanelModelCollection(),
	      heightAdjustment: 2,
	    };
	  },
	});
	
	/**
	 * @class app.views.panels.PanelLevelModelCollection
	 */
	var PanelLevelModelCollection = ViewModelCollection.extend({
	  constructor: function PanelLevelModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelLevelModel,
	});
	
	
	/**
	 * @class app.views.panels.PanelColumnModel
	 */
	var PanelColumnModel = ViewModel.extend({
	  constructor: function PanelColumnModel() {
	    ViewModel.apply(this, arguments);
	  },
	  defaults: function() {
	    return {
	      collection: new PanelLevelModelCollection(),
	    };
	  },
	});
	
	
	/**
	 * @class app.views.panels.PanelColumnModelCollection
	 */
	var PanelColumnModelCollection = ViewModelCollection.extend({
	  constructor: function PanelColumnModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelColumnModel,
	});
	
	
	/**
	 * @class app.views.panels.PanelGroupModelCollection
	 */
	var PanelGroupModelCollection = ViewModelCollection.extend({
	  constructor: function PanelGroupModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelGroupModel,
	});
	
	/**
	 * @class app.views.panels.PanelGroupModel
	 */
	var PanelGroupModel = ViewModel.extend({
	  constructor: function PanelGroupModel() {
	    ViewModel.apply(this, arguments);
	  },
	  defaults: function() {
	    return {
	      collection: new PanelColumnModelCollection(),
	    };
	  },
	});
	
	/**
	 * @class app.views.panels.PanelGroupModelCollection
	 */
	var PanelGroupModelCollection = ViewModelCollection.extend({
	  constructor: function PanelGroupModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelGroupModel,
	});
	
	/**
	 * @class app.views.panels.PanelManagerModel
	 */
	var PanelManagerModel = ViewModel.extend({
	  constructor: function PanelManagerModel() {
	    ViewModel.apply(this, arguments);
	  },
	  defaults: function() {
	    return {
	      collection: new PanelGroupModelCollection(),
	    };
	  },
	});
	
	/**
	 * @class app.views.panels.PanelManagerModelCollection
	 */
	var PanelManagerModelCollection = ViewModelCollection.extend({
	  constructor: function PanelManagerModelCollection() {
	    ViewModelCollection.apply(this, arguments);
	  },
	  model: PanelManagerModel,
	});
	
	/**
	 * An abstract class every panel should eventually extend
	 * @class app.views.views.BasePanel
	 */
	var BasePanel = Marionette.View.extend({
	  constructor: function BasePanel() {
	    Marionette.View.apply(this, arguments);
	  },
	
	  name: '',
	
	  registerClass: function() {
	    PanelManager.prototype.registerPanelClass(this);
	  },
	
	  changeSelection: function(selectionChanges) {
	    //
	  },
	
	  getAllowedPanelNames: function() {
	    return [];  // String[]
	  },
	
	  getAutoactivatedPanelNames: function() {
	      return [];  // String[]
	  },
	
	  getMinWidth: function() {
	      return 200;
	  },
	
	  getMaxWidth: function() {
	      return 1500;
	  },
	
	  getMinHeight: function() {
	      return 20;
	  },
	
	  setMinimize: function(minimize) {
	    
	  },
	
	});
	
	/**
	 * An abstract class every panel should eventually extend
	 * @class app.views.views.PanelWrapper
	 */
	var PanelWrapper = Marionette.View.extend({
	  constructor: function PanelWrapper() {
	    Marionette.View.apply(this, arguments);
	  },
	
	  ui: {
	    panel: '.panelc',
	    header: '.panelw-header',
	    minButton: '.js_min',
	  },
	  regions: {
	    panelR: '@ui.panel',
	    header: '@ui.header',
	  },
	  events: {
	    'click @ui.minButton': 'toggleMinimize',
	  },
	  className: "panel-w",
	  template: _.template("<div class='panelw-header'><%= panelName %><button class='js_min'><%= minSymbol %></button></div><div class='panelc'></div>"),
	
	  initialize: function(options) {
	    this.minimized = !!this.model.get('minimized');
	    this.panelManager = options.panelManager;
	    this.panelGroup = options.panelGroup;
	    this.panelLevel = options.panelLevel;
	    this.panelColumn = options.panelColumn;
	    this.panelColumns = options.panelColumns;
	  },
	
	  serializeData: function() {
	    return {
	      panelName: this.model.get('panelName'),
	      minSymbol: (this.minimized)?'+':'-',
	    };
	  },
	
	  onRender: function(options) {
	    var panelName = this.model.get('panelName'),
	        panel = PanelManager.prototype.createPanelByName(panelName);
	    if (panel) {
	      panel.wrapper = this;
	      this.panel = panel;
	      this.showChildView('panelR', panel);
	    } else {
	      this.ui.panel.text("Cannot find "+panelName)
	    }
	  },
	
	  onAttach: function() {
	    if (this.minimized) {
	      this.$el.addClass('minimized');
	    }
	  },
	
	  toggleMinimize: function() {
	    this.setMinimize(!this.minimized);
	    this.$el.find('.js_min').text((this.minimized)?'+':'-');
	  },
	
	  setMinimize: function(minimized) {
	    if (minimized !== this.minimized) {
	      // console.log("setting min of panel G"+this.panelGroup.indexInManager()
	      // +"C"+this.panelColumn.indexInColumns()+"L"+this.panelLevel.indexInColumn()
	      // +"P"+this.indexInLevel()+" to "+minimized);
	      if (minimized) {
	        this.$el.addClass('minimized');
	      } else {
	        this.$el.removeClass('minimized');
	      }
	      this.minimized = minimized;
	      this.model.set('minimized', minimized);
	      this.panel.setMinimize(minimized);
	      this.panelLevel.updateMinimize(this);
	      this.panelManager.updateMinimize(this);
	      this.panelManager.resetPercent();
	    }
	  },
	
	  indexInLevel: function() {
	    return this.panelLevel.panelCollection.collection.indexOf(this.model);
	  },
	
	  getAllowedPanelNames: function() {
	    return this.panel.getAllowedPanelNames();
	  },
	
	  getAutoactivatedPanelNames: function() {
	    return this.panel.getAutoactivatedPanelNames();
	  },
	
	  getMinWidth: function() {
	    return this.panel.getMinWidth();
	  },
	
	  getMaxWidth: function() {
	    return this.panel.getMaxWidth();
	  },
	
	  getMinHeight: function() {
	    return this.panel.getMinHeight() + 20;
	  },
	
	  changeSelection: function(selectionChanges) {
	    return this.panel.changeSelection(selectionChanges);
	  },
	
	});
	
	
	/**
	 * @class app.views.views.PanelCollection
	 */
	var PanelCollection = Marionette.CollectionView.extend({
	  constructor: function PanelCollection() {
	    // Is it a Marionette object or an abstraction?
	    // Clearly the former in the case of a multipanel level, at least.
	    Marionette.CollectionView.apply(this, arguments);
	  },
	  singlePanel: true,
	  className: 'panel-collection',
	  initialize: function(options) {
	    this.collection = this.model.get('collection');
	    this.panelManager = options.panelManager;
	    this.panelGroup = options.panelGroup;
	    this.panelColumn = options.panelColumn;
	    this.panelColumns = options.panelColumns;
	    this.panelLevel = options.panelLevel;
	  },
	
	  getPanelWrappers: function() {
	    return this.children;
	  },
	
	  childView: PanelWrapper,
	
	  childViewOptions: function() {
	    return {
	      panelManager: this.panelManager,
	      panelGroup: this.panelGroup,
	      panelColumn: this.panelColumn,
	      panelColumns: this.panelColumns,
	      panelLevel: this.panelLevel,
	    };
	  },
	
	  _addPanel: function(panelName, minimized) {
	    // check for duplicates? Do we allow them?
	    this.collection.push(new PanelModel({
	      panelName: panelName,
	      minimized: minimized,
	    }));
	    this.panelManager.updateMinimize();
	  },
	
	  _removePanel: function(panel) {
	    var model = this.collection.find(function(model) {
	      return model === panel.wrapper.model;
	    });
	    if (model != null) {
	      this.collection.remove(model);
	      this.panelManager.updateMinimize();
	    }
	    // panel.terminate() // or whatever needed to avoid leaks
	  },
	
	  changeSelection: function(selectionChanges) {
	    this.getPanelWrappers().each(function(panel) {
	      panel.changeSelection(selectionChanges);
	    });
	  },
	});
	
	
	
	/**
	 * @class app.views.views.PanelLevel
	 */
	var PanelLevel = Marionette.View.extend({
	  constructor: function PanelLevel() {
	    // Is it a Marionette object or an abstraction?
	    // Clearly the former in the case of a multipanel level, at least.
	    Marionette.View.apply(this, arguments);
	  },
	  template: _.template("<div class='level-header'>G<%= groupN %>C<%= columnN %>L<%= levelN %></div><div class='panels'></div>"),
	  singlePanel: true,
	  className: 'panel-level',
	  ui: {
	    panels: '.panels',
	    header: '.level-header',
	  },
	  regions: {
	    panels: '@ui.panels',
	    header: '@ui.header',
	  },
	  initialize: function(options) {
	    this.minimized = !!this.model.get('minimized');
	    this.panelManager = options.panelManager;
	    this.panelGroup = options.panelGroup;
	    this.panelColumn = options.panelColumn;
	    this.panelColumns = options.panelColumns;
	    options.panelLevel = this;
	    this.panelCollection = new PanelCollection(options);
	    this.singlePanel = options.singlePanel;
	    this.allowedPanelNames = [];
	  },
	
	  serializeData: function() {
	    return {
	      levelN: this.indexInColumn(),
	      columnN: this.panelColumn.indexInColumns(),
	      groupN: this.panelGroup.indexInManager(),
	    };
	  },
	
	  onRender: function() {
	    this.showChildView('panels', this.panelCollection);
	  },
	
	  onAttach: function() {
	    if (this.minimized) {
	      this.$el.addClass('minimized');
	    } else {
	      this.adjustModelHeight();
	    }
	  },
	  adjustModelHeight: function(heightAdjustment) {
	    if (heightAdjustment === undefined) {
	      heightAdjustment = this.model.get('heightAdjustment');
	    }
	    this.$el.css('height', 'calc(100% - '+heightAdjustment+'px)');
	  },
	  getPanelWrappers: function() {
	    return this.panelCollection.getPanelWrappers();
	  },
	
	  indexInColumn: function() {
	    // coming soon
	    return this.panelColumn.collection.indexOf(this.model);
	  },
	
	  addPanel: function(panelName) {
	    this.panelCollection._addPanel(panelName);
	    var multiPanel = (this.panelCollection.collection.length > 1);
	    if (multiPanel && this.singlePanel) {
	      console.log('error');
	      return;
	    }
	  },
	  getMinWidth: function() {
	    var panels = this.getPanelWrappers(),
	        width = 0,
	        previousIsMinimized = false;
	    panels.each(function(panel) {
	      var panelWidth = panel.getMinWidth();
	      if (previousIsMinimized) {
	        width = Math.max(width, panelWidth);
	      } else {
	        width += panelWidth;
	      }
	      previousIsMinimized = panel.minimized;
	    });
	    return width;
	  },
	  getMaxWidth: function() {
	    var panels = this.getPanelWrappers(),
	        width = 0,
	        previousIsMinimized = false;
	    panels.each(function(panel) {
	      var panelWidth = panel.getMaxWidth();
	      if (previousIsMinimized) {
	        width = Math.min(width, panelWidth);
	      } else {
	        width += panelWidth;
	      }
	      previousIsMinimized = panel.minimized;
	    });
	    return width;
	  },
	  getMinHeight: function() {
	    var panels = this.getPanelWrappers(),
	        height = 0;
	    panels.each(function(wrapper) {
	      height += wrapper.getMinHeight();
	    });
	    return height;
	  },
	  updateMinimize: function(panel) {
	    var minimized = this.getPanelWrappers().all(function(p) {
	      return p.minimized;
	    });
	    if (minimized !== this.minimized) {
	      // console.log("setting min of level G"+this.panelGroup.indexInManager()
	      // +"C"+this.panelColumn.indexInColumns()+"L"+this.indexInColumn()+" to "+minimized);
	      if (minimized) {
	        this.$el.addClass('minimized');
	        panel.$el.css('height', '');
	      } else {
	        this.$el.removeClass('minimized');
	      }
	      this.minimized = minimized;
	      this.model.set('minimized', minimized);
	      this.panelColumns.updateMinimize(this);
	      this.panelGroup.updateMinimize(panel);
	    }
	  },
	
	  nextPanelToMinimize: function() {
	    return this.getPanelWrappers().find(function(panel) {
	      return !panel.minimized;
	    });
	  },
	
	  nextPanelToUnminimize: function() {
	    var panels = this.getPanelWrappers()
	    // reverse
	    panels = panels.last(panels.length);
	    return _.find(panels, function(panel) {
	      return panel.minimized;
	    });
	  },
	
	  removePanel: function(panel) {
	    this.panelCollection._removePanel(panel);
	  },
	
	  changeSelection: function(selectionChanges) {
	    this.panelCollection.changeSelection(selectionChanges);
	  },
	
	  resetWithNames: function(allowedPanelNames, autoactivatedPanelNames) {
	    var that = this,
	        change = false,
	        panels = this.getPanelWrappers(),
	        numActive = panels.length;
	    panels.each(function(panel) {
	      if (!_.contains(allowedPanelNames, panel.panel.name)) {
	        that.removePanel(panel.panel);
	        numActive -= 1;
	        change = true;
	      }
	    });
	    // assumption: Only autoactivate if nothing active.
	    if (autoactivatedPanelNames.length && !numActive) {
	      this.addPanel(autoactivatedPanelNames[0]);
	      numActive += 1;
	      change = true;
	    }
	    this.allowedPanelNames = allowedPanelNames;
	    return change;
	  },
	});
	
	
	/**
	 * PanelColumn aka PanelLevelCollection
	 * @class app.views.views.PanelColumn
	 */
	var PanelColumn = Marionette.CollectionView.extend({
	  constructor: function PanelColumn() {
	    Marionette.CollectionView.apply(this, arguments);
	  },
	  initialize: function(options) {
	    this.rootName = options.rootName;
	    this.panelManager = options.panelManager;
	    this.panelGroup = options.panelGroup;
	    this.panelColumns = options.panelColumns;
	    this.collection = this.model.get('collection');
	  },
	  indexInColumns: function() {
	    return this.panelColumns.collection.indexOf(this.model);
	  },
	  className: 'panel-column',
	  childView: PanelLevel,
	  getLevels: function() {
	    return this.children;
	  },
	  getSelection: function() {
	    return this.panelGroup.getSelection();
	  },
	  pushLevel: function() {
	    this.collection.add(new PanelLevelModel());
	  },
	  childViewOptions: function(view, index) {
	    return {
	      panelManager: this.panelManager,
	      panelGroup: this.panelGroup,
	      panelColumns: this.panelColumns,
	      panelColumn: this,
	    };
	  },
	  removeLastLevel: function() {
	    this.collection.pop();
	  },
	  getLastLevel: function() {
	    var lastModel = this.collection.last();
	    if (lastModel) {
	      return this.children.findByModel(lastModel);
	    }
	  },
	  getMinWidth: function() {
	    var levels = this.getLevels(),
	        width = 0,
	        previousIsMinimized = false;
	    levels.each(function(level) {
	      var levelWidth = level.getMinWidth();
	      if (previousIsMinimized) {
	        width = Math.min(width, levelWidth);
	      } else {
	        width += levelWidth;
	      }
	      previousIsMinimized = level.minimized;
	    });
	    return width;
	  },
	  adjustLevelHeight: function() {
	    var lastLevelModel = this.collection.last(),
	        lastLevel = this.children.findByModel(lastLevelModel),
	        minHeight = 2 + this.getMinimizedHeight();
	    console.log("adjusting level G"+this.panelGroup.indexInManager()+"C"+this.indexInColumns()+"L"+lastLevel.indexInColumn()+" to "+minHeight);
	    lastLevelModel.set('heightAdjustment', minHeight);
	    lastLevel.adjustModelHeight(minHeight);
	  },
	  getMaxWidth: function(panel) {
	    var levels = this.getLevels(),
	        width = 0,
	        previousIsMinimized = false;
	    levels.each(function(level) {
	      var levelWidth = level.getMaxWidth();
	      if (previousIsMinimized) {
	        width = Math.min(width, levelWidth);
	      } else {
	        width += levelWidth;
	      }
	      previousIsMinimized = level.minimized;
	    });
	    return width;
	  },
	  getMinimizedHeight: function() {
	    var levels = this.getLevels(),
	        height = 0;
	    levels.each(function(level) {
	      if (level.minimized) {
	        height += level.getMinHeight();
	      }
	    });
	    return height;
	  },
	  nextLevel: function(level) {
	    var i = this.collection.indexOf(level.model);
	    if (i < this.children.length - 1) {
	      return this.children.findByModel(this.collection.at(i+1));
	    }
	  },
	  resetPercent: function(minWidth) {
	    var myMinWidth = this.getMinWidth();
	    this.$el.css("width", (100.0*myMinWidth/minWidth)+"%");
	  },
	});
	
	
	/**
	 * @class app.views.views.PanelColumnCollection
	 */
	var PanelColumnCollection = Marionette.CollectionView.extend({
	  constructor: function PanelColumnCollection() {
	    Marionette.CollectionView.apply(this, arguments);
	  },
	  initialize: function(options) {
	    this.rootName = options.rootName;
	    this.panelManager = options.panelManager;
	    this.panelGroup = options.panelGroup;
	    this.rootName = options.rootName;
	    this.collection = this.model.get('collection');
	  },
	  className: 'panel-column-collection',
	  childView: PanelColumn,
	  getColumns: function() {
	    return this.children;
	  },
	  getLevels: function() {
	    var that = this,
	        levels = [];
	    // costly for no good reason.
	    this.collection.each(function(columnModel) {
	      var column = that.children.findByModel(columnModel);
	      column.collection.each(function(levelModel) {
	        var level = column.children.findByModel(levelModel);
	        levels.push(level);
	      });
	    });
	    return levels;
	  },
	  getLevelByIndex: function(i) {
	    var column = this.children.find(function(column) {
	      if (i >= column.children.length) {
	        i -= column.children.length;
	        return false;
	      } else {
	        return true;
	      }
	    });
	    if (column) {
	      return column.children.findByModel(column.collection.at(i));
	    }
	  },
	  nextColumn: function(column) {
	    var i = this.collection.indexOf(column.model);
	    if (i < this.children.length - 1) {
	      return this.children.findByModel(this.collection.at(i+1));
	    }
	  },
	  previousColumn: function(column) {
	    var i = this.collection.indexOf(column.model);
	    if (i > 0) {
	      return this.children.findByModel(this.collection.at(i-1));
	    }
	  },
	  nextLevel: function(level) {
	    var other = level.panelColumn.nextLevel(level);
	    if (other) {
	      return other;
	    }
	    other = this.nextColumn(level.panelColumn);
	    if (other) {
	      return other.children[0];
	    }
	  },
	  countLevels: function() {
	    var numLevels = 0;
	    this.children.each(function(column) {
	      numLevels += column.collection.length;
	    });
	    return numLevels;
	  },
	  getSelection: function() {
	    return this.panelGroup.getSelection();
	  },
	  childViewOptions: function(view, index) {
	    return {
	      panelManager: this.panelManager,
	      panelGroup: this.panelGroup,
	      rootName: this.rootName,
	      panelColumns: this,
	    };
	  },
	  pushColumn: function() {
	    this.collection.add(new PanelColumnModel());
	  },
	  pushLevel: function() {
	    this.pushColumn();
	    this.children.last().pushLevel();
	  },
	  removeLastLevel: function() {
	    assert(this.collection.length > 0, "no columns?");
	    var columnModel = this.collection.last(),
	        view = this.children.findByModel(columnModel);
	    assert(view.collection.length > 0, "no level in column?");
	    view.removeLastLevel();
	    if (view.getLevels().length == 0) {
	      this.collection.pop();
	    }
	  },
	  changeSelection: function(selectionChanges) {
	    var numLevels = this.countLevels(),
	        allowedPanelNames = [this.rootName],
	        autoactivatedPanelNames = allowedPanelNames,
	        pos = 0,
	        level,
	        change = false,
	        autoactivate = true;
	    while (autoactivate) {
	      while (pos >= numLevels) {
	        this.pushLevel();
	        numLevels++;
	        change = true;
	      }
	      level = this.getLevelByIndex(pos++);
	      change = level.resetWithNames(allowedPanelNames, autoactivatedPanelNames) || change;
	      allowedPanelNames = [];
	      autoactivate = false;
	      autoactivatedPanelNames = [];
	      level.getPanelWrappers().each(function(panel) {
	        panel.changeSelection(selectionChanges);
	        allowedPanelNames = allowedPanelNames.concat(panel.getAllowedPanelNames());
	        autoactivatedPanelNames = autoactivatedPanelNames.concat(panel.getAutoactivatedPanelNames());
	      });
	      if (allowedPanelNames.length === 0) {
	        while (numLevels > pos) {
	          this.removeLastLevel();
	          numLevels--;
	          change = true;
	        }
	        break;
	      }
	      autoactivate = autoactivatedPanelNames.length > 0;
	      // remove duplicates in autoactivatedPanelNames/allowedPanel names, but keep order.
	      // Make sure autoactivated panel names are in the front of allowedPanelNames.
	      // Not sure how to handle different priorities... as things
	      // stand, first panel dominates. Maybe interleave? Rarely an issue.
	    }
	    if (change) {
	      this.panelManager.resetPercent();
	    }
	  },
	
	  nextPanelToMinimize: function() {
	    var that = this,
	        panels = [];
	    this.collection.each(function (model) {
	      var column = that.children.findByModel(model);
	      column.collection.each(function(levelModel) {
	        var level = column.children.findByModel(levelModel),
	            panel = level.nextPanelToMinimize();
	        if (panel) {
	          panels.push(panel);
	        }
	      });
	    });
	    if (panels.length) {
	      return panels[0];
	    }
	  },
	  nextPanelToUnminimize: function() {
	    var that = this,
	        panels = [];
	    this.collection.each(function (model) {
	      var column = that.children.findByModel(model);
	      column.collection.each(function(levelModel) {
	        var level = column.children.findByModel(levelModel),
	            panel = level.nextPanelToUnminimize();
	        if (panel) {
	          panels.push(panel);
	        }
	      });
	    });
	    if (panels.length) {
	      // TODO: Sort by depth
	      panels.reverse();
	      return panels[0];
	    }
	  },
	  getMinWidth: function() {
	    var columns = this.getColumns(),
	        width = 0;
	    columns.each(function(column) {
	      width += column.getMinWidth();
	    });
	    return width;
	  },
	  getMaxWidth: function() {
	    var columns = this.getColumns(),
	        width = 0;
	    columns.each(function(column) {
	      width += column.getMaxWidth();
	    });
	    return width;
	  },
	  updateMinimize: function(panelLevel) {
	    if (panelLevel.minimized) {
	      // level was just minimized, recreate that panel and all panels
	      // of that column (should all be minimized)
	      // in the next column (if any.)
	      assert(panelLevel.indexInColumn()
	        == panelLevel.panelColumn.collection.length - 1,
	        "should be last level");
	      var sourceCol = panelLevel.panelColumn,
	          targetCol = this.nextColumn(sourceCol);
	      if (targetCol) {
	        var models = sourceCol.collection.models.slice();
	        if (models.length > 1) {
	          assert(_.all(models, function (model) {
	            return !!model.get('minimized');
	          }), "previous models should be minimized");
	        }
	        sourceCol.collection.remove(models);
	        targetCol.collection.add(models, {at: 0});
	        this.collection.remove(sourceCol.model);
	        targetCol.adjustLevelHeight();
	        this.render();
	      }
	    } else {
	      // level was just maximized, shift it (and previous minimized levels)
	      // to new previous column. Not needed if last level
	      var nextLevel = this.nextLevel(panelLevel);
	      if (nextLevel) {
	        var colNum = panelLevel.panelColumn.indexInColumns();
	        this.collection.add(new PanelColumnModel(), {at: colNum});
	        var sourceCol = panelLevel.panelColumn,
	            targetCol = this.children.findByModel(this.collection.at(colNum)),
	            levelIndex = panelLevel.indexInColumn(),
	            models = sourceCol.collection.models.slice(0, levelIndex + 1);
	        sourceCol.collection.remove(models);
	        sourceCol.adjustLevelHeight();
	        targetCol.collection.add(models);
	        targetCol.adjustLevelHeight();
	      }
	    }
	  },
	  resetPercent: function(minWidth) {
	    this.children.each(function(column) {
	      column.resetPercent(minWidth);
	    });
	  },
	});
	
	
	/**
	 * @class app.views.views.PanelGroup
	 */
	var PanelGroup = Marionette.View.extend({
	  constructor: function PanelGroup() {
	    Marionette.View.apply(this, arguments);
	  },
	  template: _.template("<div class='group-header'>G<%= groupN %><button class='closeButton'>x</button></div><div class='columns'></div>"),
	  ui: {
	    closeButton: ".closeButton",
	    columns: ".columns",
	  },
	  regions: {
	    columns: "@ui.columns",
	  },
	  initialize: function(options) {
	    this.minimized = !!this.model.get('minimized');
	    this.rootName = options.rootName;
	    this.collection = this.model.get('collection');
	    this.panelManager = options.panelManager;
	    options.panelGroup = this;
	    this.columnsC = new PanelColumnCollection(options);
	    this.selection = {};
	  },
	  className: 'panel-group',
	  rootName: '',
	
	  indexInManager: function() {
	    return this.panelManager.collection.indexOf(this.model);
	  },
	
	  updateMinimize: function(panel) {
	    // TODO: Rewrite as columns
	    var minimized = _.all(this.getLevels(), function(p) {
	      return p.minimized;
	    });
	    if (minimized !== this.minimized) {
	      // console.log("setting min of group G"+this.indexInManager()+" to "+minimized);
	      if (minimized) {
	        this.$el.addClass('minimized');
	      } else {
	        this.$el.removeClass('minimized');
	      }
	      this.minimized = minimized;
	    }
	  },
	
	  serializeData: function() {
	    return {
	      groupN: this.indexInManager(),
	    };
	  },
	
	  getLevels: function() {
	    return this.columnsC.getLevels();
	  },
	  getSelection: function() {
	    return this.selection;
	  },
	  onRender: function() {
	    this.showChildView('columns', this.columnsC);
	  },
	  removeLastLevel: function() {
	    this.columnsC.removeLastLevel();
	  },
	  nextPanelToMinimize: function() {
	    return this.columnsC.nextPanelToMinimize();
	  },
	  nextPanelToUnminimize: function() {
	    return this.columnsC.nextPanelToUnminimize();
	  },
	  getMinWidth: function() {
	    return this.columnsC.getMinWidth();
	  },
	  getMaxWidth: function(panel) {
	    return this.columnsC.getMaxWidth();
	  },
	  changeSelection: function(selectionChanges) {
	    _.extend(this.selection, selectionChanges);
	    return this.columnsC.changeSelection(selectionChanges);
	  },
	  resetPercent: function(minWidth) {
	    var myMinWidth = this.getMinWidth();
	    this.$el.css("width", (100.0*myMinWidth/minWidth)+"%");
	    this.columnsC.resetPercent(myMinWidth);
	  },
	});
	
	
	/**
	 * @class app.views.views.PanelManager
	 */
	var PanelManager = Marionette.CollectionView.extend({
	  constructor: function PanelManager() {
	    Marionette.CollectionView.apply(this, arguments);
	  },
	  className: 'panel-manager fitting',
	  leftMargin: 5,
	  rightMargin: 5,
	  groupMargin: 5,
	  fitToWindow: true,
	  childView: PanelGroup,
	  initialize: function(options) {
	    this.rootName = options.rootName;
	    this.model = new PanelManagerModel();
	    this.collection = this.model.get('collection');
	    this.collection.add(new PanelGroupModel());
	    this.resetPercent();
	  },
	  childViewOptions: function(view, index) {
	    return {
	      rootName: this.rootName,
	      panelManager: this,
	    };
	  },
	  getGroups: function() {
	    return this.children;
	  },
	  panelClassesByName: new Object(),
	  registerPanelClass: function(cls) {
	    // called on the prototype
	    this.panelClassesByName[cls.prototype.name] = cls;
	  },
	  createPanelByName: function(name) {
	    // called on the prototype
	    var cls = this.panelClassesByName[name];
	    if (cls != null) {
	      return new cls(arguments);
	    }
	  },
	
	  canFit: function(width) {
	    var minWidth = this.getMinWidth(); // ordered somehow
	    return minWidth <= width;
	  },
	  setFitToWindow: function(fitToWindow) {
	    if (this.fitToWindow !== fitToWindow) {
	      if (fitToWindow) {
	        this.$el.addClass('fitting');
	      } else {
	        this.$el.removeClass('fitting');
	      }
	      this.fitToWindow = fitToWindow;
	    }
	    // and recalc css if actually changed.
	  },
	  updateMinimize: function(panel) {
	    var canFit = this.canFit(window.innerWidth);
	    if (this.fitToWindow !== canFit) {
	      this.setFitToWindow(canFit);
	    }
	  },
	  getMinWidth: function(panel) {
	    var groups = this.getGroups(),
	        previousIsMinimized = false,
	        margin = this.groupMargin,
	        width = -margin;
	    groups.each(function(group) {
	      var groupWidth = group.getMinWidth();
	      if (previousIsMinimized) {
	        width = Math.min(width, groupWidth);
	      } else {
	        width += groupWidth + margin;
	      }
	      previousIsMinimized = group.minimized;
	    });
	    return width + this.leftMargin + this.rightMargin;
	  },
	
	  getMaxWidth: function(panel) {
	    var groups = this.getGroups(),
	        previousIsMinimized = false,
	        margin = this.groupMargin,
	        width = -margin;
	    groups.each(function(group) {
	      var groupWidth = group.getMaxWidth();
	      if (previousIsMinimized) {
	        width = Math.min(width, groupWidth);
	      } else {
	        width += groupWidth + margin;
	      }
	      previousIsMinimized = group.minimized;
	    });
	    return width + this.leftMargin + this.rightMargin;
	  },
	
	  getMaxWidth: function(panel) {
	    var groups = this.getGroups(),
	        width = this.groupMargin * (groups.length - 1) + this.leftMargin + this.rightMargin;
	    groups.each(function(group) {
	      width += group.getMaxWidth();
	    });
	    return width;
	  },
	  nextPanelToMinimize: function() {
	    var groups = this.getGroups(),
	        panels = [];
	    groups.each(function(group) {
	      var panel = group.nextPanelToMinimize();
	      if (panel != null) {
	        panels.push(panel);
	      }
	    });
	    // TODO: Choose the one with the lowest depth... ideally not the latest active group?
	    if (panels.length) {
	      return panels[0];
	    }
	  },
	  nextPanelToUnminimize: function() {
	    var groups = this.getGroups(), panels = [];
	    groups.each(function(group) {
	      var panel = group.nextPanelToUnminimize();
	      if (panel != null) {
	        panels.push(panel);
	      }
	    });
	    // TODO: Choose the one with the lowest depth... ideally not the latest active group?
	    if (panels.length) {
	      return panels[0];
	    }
	  },
	  resetPercent: _.throttle(function() {
	    var minWidth = this.getMinWidth();
	    this.children.each(function(group) {
	      group.resetPercent(minWidth);
	    });
	  }, 100, { leading: false }),
	  resize: _.throttle(function(newWidth) {
	      // cases:
	      // not fitting, growing: see if fits. if so, fall to next step.
	      // fit, growing: unminimize while fits.
	      // fit, growing smaller: if stops fitting, minimize until fits? not sure.
	      // not fitting, growing smaller: do nothing.
	      // TODO: Add a delay function to this, and make sure it does not happen too often
	      var nextPanelWidth,
	          change = false,
	          minWidth = this.getMinWidth(),
	          canFit = minWidth <= newWidth;
	      while (canFit) {
	        var panel = this.nextPanelToUnminimize();
	        if (panel == undefined) {
	          // TODO Can we minimize a group, in that case?
	          break;
	        }
	        nextPanelWidth = panel.getMinWidth();
	        if (minWidth + nextPanelWidth > newWidth) {
	          break;
	        }
	        panel.setMinimize(false);
	        change = true;
	        minWidth = this.getMinWidth();
	        canFit = this.canFit(newWidth);
	      }
	      if (this.fitToWindow && ! canFit) {
	        while (!canFit) {
	          var panel = this.nextPanelToMinimize();
	          if (panel == undefined) {
	            break;
	          }
	          panel.setMinimize(true);
	        change = true;
	          minWidth = this.getMinWidth();
	          canFit = this.canFit(newWidth);
	        }
	      }
	      if (canFit && !this.fitToWindow) {
	        this.setFitToWindow(canFit);
	      }
	      if (change) {
	        this.resetPercent();
	      }
	  }, 100, { leading: false }),
	});
	
	
	module.exports = {
	  BasePanel: BasePanel,
	  PanelLevel: PanelLevel,
	  PanelManager: PanelManager,
	  PanelGroup: PanelGroup,
	};

/***/ }

});
//# sourceMappingURL=panelTest.js.map