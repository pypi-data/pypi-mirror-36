"use strict";

var voteApp = angular.module('voteApp',
    ['ngRoute', 'ngSanitize', 'voteServices', 'pascalprecht.translate', 'mgcrea.ngStrap.datepicker', 'mgcrea.ngStrap.timepicker']);

voteApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
        when('/', {
          templateUrl:'app/partials/index.html',
          controller:'indexCtl'
        }).
        when('/voted', {
          templateUrl:'app/partials/voted.html',
          controller:'votedCtl'
        }).
        when('/results', {
          templateUrl:'app/partials/results.html',
          controller:'resultsCtl'
        }).
        when('/admin', {
          templateUrl:'app/partials/admin.html',
          controller:'adminCtl'
        }).
        when('/admin/create_from_idea', {
          templateUrl:'app/partials/admin_create_from_idea.html',
          controller:'adminCreateFromIdeaCtl'
        }).
        when('/admin/configure_instance', {
          templateUrl:'app/partials/admin_configure_instance.html',
          controller:'adminConfigureInstanceCtl'
        }).
        when('/admin/configure_instance_set_criteria', {
          templateUrl:'app/partials/admin_configure_instance_set_criteria.html',
          controller:'adminConfigureInstanceSetCriteriaCtl'
        }).
        when('/admin/configure_instance_set_votable_ideas', {
          templateUrl:'app/partials/admin_configure_instance_set_votable_ideas.html',
          controller:'adminConfigureInstanceSetVotableIdeasCtl'
        }).
        when('/admin/configure_instance_set_settings', {
          templateUrl:'app/partials/admin_configure_instance_set_settings.html',
          controller:'adminConfigureInstanceSetSettingsCtl'
        }).
        when('/admin/configure_instance_set_start_and_end_dates', {
          templateUrl:'app/partials/admin_configure_instance_set_start_and_end_dates.html',
          controller:'adminConfigureInstanceSetStartAndEndDatesCtl'
        }).
        otherwise({
          redirectTo: '/'
        });

}]);


// returns the value of a given parameter in the URL of the current page
function getUrlVariableValue(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      return pair[1];
    }
  } 

  //alert('Query Variable ' + variable + ' not found');
  return null;
}
window.getUrlVariableValue = getUrlVariableValue;


voteApp.config(['$translateProvider', function($translateProvider) {
  $translateProvider.useStaticFilesLoader({
    prefix: 'app/locales/',
    suffix: '.json'
  });

  // language detection and fallbacks

  $translateProvider.fallbackLanguage('en');
  $translateProvider.registerAvailableLanguageKeys(['en', 'fr'], {
    'en_US': 'en',
    'en_UK': 'en',
    'de_DE': 'en',
    'de': 'en',
    'de_CH': 'en',
    'en-US': 'en',
    'en-UK': 'en',
    'de-DE': 'en',
    'de-CH': 'en',
    'fr_FR': 'fr',
    'fr-fr': 'fr',
  });

  //$translateProvider.preferredLanguage('fr'); // no, we want to use one of the available languages
  //$translateProvider.determinePreferredLanguage(); // not enough: any language not listed in registerAvailableLanguageKeys() won't use fallback, resulting in translation keys appearing on the page
  var getLocale = function() {
      var nav = window.navigator;
      return (nav.language || nav.browserLanguage || nav.systemLanguage || nav.userLanguage || '').split('-').join('_');
    };
  var localeOrFallback = function(locale) {
    if (locale && locale.length && locale.length > 2)
        locale = locale.substring(0, 2);
    locale = locale.toLowerCase();
    if (locale != 'fr')
        locale = 'en';
    return locale;
  };
  $translateProvider.determinePreferredLanguage(function() {
    var locale;
    var localeInUrl = window.getUrlVariableValue("locale");
    console.log("localeInUrl: ", localeInUrl);
    if (localeInUrl)
        locale = localeInUrl;
    else
        locale = getLocale();
    locale = localeOrFallback(locale);
    console.log("determined locale: ", locale);
    return locale;
  });

}]);

voteApp.provider('configService', function() {
  var options = {};
  this.config = function(opt) {
    angular.extend(options, opt);
  };
  this.$get = [function() {
    if (!options)
    {
      throw new Error('Config options must be configured');
    }

    return options;
  }];
});

voteApp.run(['configTestingService', function(configTestingService) {
  //configTestingService.init();
}]);

// Before initializing manually Angular, we get the config of the widget, by accessing the "config" parameter of the current URL
// For example: http://localhost:6543/widget/vote/?config=http://localhost:6543/data/Widget/19#/
angular.element(document).ready(function() {
  console.log("angular.element(document).ready()");
  // Tell Explorer not to cache Ajax requests.
  $.ajaxSetup({ cache: false });

  function startAngularApplication() {
    angular.bootstrap('#voteApp', ['voteApp']);
  }

  // TODO: find a way to have only one such function somewhere instead of one here and one in services.js
  function resourceToUrl(str) {
    var start = "local:";
    if (str && str.indexOf(start) == 0) {
      str = "/data/" + str.slice(start.length);
    }

    return str;
  };

  // TODO: better way to access the admin panel
  // if the user is trying to access the admin panel, skip the loading of the configuration file and start the Angular application directly
  var admin_variable = window.getUrlVariableValue("admin");
  console.log("admin_variable:");
  console.log(admin_variable);
  if (admin_variable != null)
  {
    startAngularApplication();
    return;
  }

  // get the "target" URL parameter
  // this parameter is meant to contain the identifier of the item about which the user is voting
  var target = window.getUrlVariableValue("target");
    
  var successCallback = function(configData) {
    console.log("successCallback ()");
    voteApp.config(['configServiceProvider', function(configServiceProvider) {
      console.log("configServiceProvider config()");
      configServiceProvider.config(configData);

      // save (or override) the "target" URL parameter into the config
      if (target != null || !configServiceProvider.target)
      {
        configServiceProvider.config({"target": target});
      }
    }]);
    startAngularApplication();
  };

  var configFileDefault = "/data/Widget/19";
  var configFile = decodeURIComponent(window.getUrlVariableValue("config"));
  configFile = resourceToUrl(configFile);
    
  if (
    !configFile
    ||
    (
      !(/^http(s)?:\/\/.*/.test(configFile))
      && !(/^\/.*/.test(configFile))
    )
  ) {
    alert("Please provide a valid URL in the 'config' parameter");
    configFile = configFileDefault;
  }

  // TODO: implement an error callback, in case the config URL given is invalid or there is a network error
  var errorCallback = function(jqXHR, textStatus, errorThrown) {
      console.log("error");
      console.log("jqXHR:");
      console.log(jqXHR);
      console.log("textStatus:");
      console.log(textStatus);
      console.log("errorThrown:");
      console.log(errorThrown);

      var error_code = jqXHR.status;
      var error_content = jqXHR.responseText;
      
      console.log("error_code:");
      console.log(error_code);
      console.log("error_content:");
      console.log(error_content);

      alert("Error while trying to load the configuration file.\nError code: " + error_code + "\nError thrown: " + errorThrown + "\nError content:" + error_content);
    };

  // if the "target" URL parameter is set, pass it along when calling the widget configuration file
  var data = {};
  if (target)
    data.target = target;
  $.get(configFile, data, successCallback).fail(errorCallback);
});

// from http://stackoverflow.com/questions/16630471/how-can-i-invoke-encodeuricomponent-from-angularjs-template
voteApp.filter('encodeURIComponent', function($window) {
    return $window.encodeURIComponent;
});
