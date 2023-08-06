'use strict';

HomeModule.controller('HomeController', [
    '$rootScope',
    '$scope',
    'config',
    'CardGameService',
    '$timeout',
    '$sce',
    'UtilsService',
    '$http',
    'growl',
    '$translate',

    function($rootScope, $scope, config, CardGameService, $timeout, $sce, UtilsService, $http, growl, $translate) {

      $rootScope.selectedComments = undefined;
      $scope.locale = $scope.locale || $rootScope.locale;
      $scope.widget = config;
      $scope.formData = {};
      $scope.displayed_cards = [];
      $scope.displayed_card_index = 0;
      $scope.avatar_size = 30;
      $scope.user_avatar_url = (("user" in $scope.widget) && ("avatar_url_base" in $scope.widget.user)) ? $scope.widget.user.avatar_url_base + "" + $scope.avatar_size : null;

      // when the session end up, switch to read only mode
      $scope.readOnly = config.activity_state !== "active";

      $scope.$watch("message", function(value) {

        switch (value) {
          case 'sendNewIdea:success':
            $translate("Thank you for your contribution! Do you have more ideas?").then(function (tr) {
              growl.success(tr);
            });
            $scope.getSubIdeaFromIdea();
            $scope.message = null; // reset message value, in order to hear another change if the user posts another message
            break;
          case 'sendNewIdea:error':
            $translate("Sorry, an error occured").then(function (tr) {
              growl.error(tr);
            });
            $scope.message = null; // reset message value, in order to hear another change if the user posts another message
            break;

        }
      }, true);

      /**
       * Fetch all ideas newly added
       */
      $scope.getSubIdeaFromIdea = function() {

        var rootUrl = UtilsService.getURL($scope.widget.ideas_url),
            ideas = [];

        $scope.parentIdeaTitle = $scope.widget.base_idea.shortTitle;

        $http.get(rootUrl).then(function(response) {

          angular.forEach(response.data, function(item) {
            if (item.widget_add_post_endpoint) {
              var widgetName = $scope.widget['@id'];
              item.widget_add_post_endpoint = UtilsService.getURL(item.widget_add_post_endpoint[widgetName]);
              item.beautify_date = UtilsService.getNiceDateTime(item.created);
              ideas.push(item);
            }
          });

          return ideas;

        }).then(function(ideas) {

          angular.forEach(ideas, function(idea) {
            var urlRoot = UtilsService.getURL(idea.proposed_in_post.idCreator);

            $http.get(urlRoot).then(function(response) {
              idea.username = response.data.name;
              idea.avatar = response.data.avatar_url_base + '30';
            });

          });

          $scope.ideas = ideas;
        });
      };

      /**
       * @params type {string}
       * @params short_title {string}
       * @params definition {string}
       * */
      $scope.sendSubIdea = function() {
        if ($scope.formData) {

          var rootUrl = UtilsService.getURL($scope.widget.ideas_hiding_url),
              random_index = angular.element('.random_index');

          $scope.formData["@type"] = 'GenericIdeaNode';
          var inspirationSourceUrl = "/static/widget/card/?#/card?deck=" + $scope.deck_pseudo_url + "&card=" + $scope.displayed_cards[$scope.displayed_card_index].originalIndex;
          $scope.formData.proposed_in_post = {
            "@type": "IdeaProposalPost",
            metadata: {
              inspiration_url: inspirationSourceUrl
            }
          };
          $scope.formData.widget_links = [
            {
              "@type": "GeneratedIdeaWidgetLink",
              context_url: inspirationSourceUrl
            }
          ];


          $http({
            method: 'POST',
            url: rootUrl,
            data: $scope.formData,
            headers: {'Content-Type': 'application/json'}
          }).success(function() {

            $scope.message = "sendNewIdea:success";
            $scope.formData.shortTitle = null;
            $scope.formData.definition = null;

          }).error(function() {

            $scope.message = "sendNewIdea:error";
          });
        }
      };

      // download the deck of cards from widget settings, or from URL parameter
      var available_decks = CardGameService.available_decks;
      var default_deck_url = available_decks[0].url;
      $scope.deck_pseudo_url = default_deck_url; // for retro-compatibility
      if ($scope.widget && "settings" in $scope.widget && "card_module_settings" in $scope.widget.settings && "deck_pseudo_url" in $scope.widget.settings.card_module_settings) {
        $scope.deck_pseudo_url = $scope.widget.settings.card_module_settings.deck_pseudo_url;
      }

      var deck_promise = CardGameService.getGenericDeck($scope.deck_pseudo_url);

      deck_promise.success(function(data) {
        $scope.game = data.game;
        $scope.shuffledCards = angular.copy($scope.game);
        for (var i = 0; i < $scope.shuffledCards.length; ++i)
        {
          $scope.shuffledCards[i].originalIndex = i;
          $scope.shuffledCards[i].body = $sce.trustAsHtml($scope.shuffledCards[i].body);
        }

        $scope.shuffleArray($scope.shuffledCards);
        $scope.pickNextCard();
      }).error(function() {
        alert("Error: Could not load requested deck of cards: " + $scope.deck_pseudo_url);
      });

      /**
       * Card random
       * */
      $scope.shuffle = function() {

        var n_cards = $scope.game.length;
        if (n_cards > 0) {
          $scope.random_index = Math.floor((Math.random() * n_cards));
          $scope.displayed_cards.push($scope.game[$scope.random_index]);
          $scope.displayed_card_index = $scope.displayed_cards.length - 1;
          $scope.displayed_cards[$scope.displayed_card_index].body = $sce.trustAsHtml($scope.game[$scope.random_index].body);
          $scope.game.splice($scope.random_index, 1);
        }
      };

      //+ Jonas Raoni Soares Silva
      //@ http://jsfromhell.com/array/shuffle [rev. #1]
      $scope.shuffleArray = function(v) {
        for (var j, x, i = v.length; i; j = parseInt(Math.random() * i), x = v[--i], v[i] = v[j], v[j] = x);
        return v;
      };

      $scope.pickNextCard = function() {
        var n_cards = $scope.game.length;
        if (n_cards > 0) {
          $scope.game.splice(0, 1);
          $scope.displayed_card_index = $scope.displayed_cards.length;
          $scope.displayed_cards.push($scope.shuffledCards[$scope.displayed_card_index]);
                
        }

        //console.log("$scope.displayed_cards: ", $scope.displayed_cards);
        //console.log("$scope.displayed_card_index: ", $scope.displayed_card_index);
      }

      /**
       * Due to the latency to init $rootScope we need a delay
       * */
      $timeout(function() {

        $scope.getSubIdeaFromIdea();

        //$scope.setJeton();

      }, 1000);

    }]);
