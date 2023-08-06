# Widgets

DRAFT DOCUMENT.
This corresponds to desired implementation, not necessarily to current implementation.

The widget architecture is meant to be as lightweight as possible.
The shared knowledge between the platform and the widget should be kept to a minimum.
Still, there is some shared knowledge. Here are a few points, with notes on Assembl implantation.

## Widget data structure

A Widget consist of the following elements: 

1. HTML/Javascript code, callable at a few addresses: At least a `widget_configuration` URL and a `widget_display` URL.
2. Server-side widget information, available as JSON from a `widget_info` URL.

Internally, there MAY also be a `widget_collection` URL, which is an endpoint to which a widget manager would POST basic Widget information to create a Widget instance's `widget_info` URL. But Widget manager logic is platform-side, and may use this or any other mechanism.

The Widget information MUST contain API endpoints for all information the Widget needs, and MAY contain some of that information directly, to save on calls. In particular, Widget information MUST contains endpoints for GETting and PUTting `settings` and `user_state` information (JSON blobs, described later), and SHOULD contain the settings directly. PUTting information on the `widget_info` URL is not guaranteed to be meaningful.

In Assembl, the Widget information also contains the current user, its permissions, and the current discussion; there MAY also be an endpoint for a generic, publically writable `widget_state` (deprecated). It is not mandatory to include any of this information directly, but URLs to GET this information should always be provided.

The `settings` information is a JSON blob, writable by the discussion administrator, readable by all, whose semantics is known by the Widget.
The `user_state` information is a JSON blob, where each user gets to write a private copy. The Widget MUST offer an endpoint to read all `users_state` of all users; no secure information should be PUT there. (Question: Do we also need a private User information store?)

## Creation of Widget settings

### Creation of an empty widget settings.

This is always the first step. Upon instantiation of a Widget, The platform will create a server-side structure with any information it needs (notably its representation of the widget @type.), and an endpoint for `widget_info`. The platform may choose to pre-populate the settings.

### Configuring the Widget Settings

The Widget expects to be called at the `widget_configuration` endpoint with an initial URL (in the `config` get variable) that yields a JSON on GET.
That URL MAY be given as absolute URLs, or relative to the server root.
They are currently in abbreviated form with a local: prefix, but this is deprecated.
The Widget MAY have a fallback settings URL of its own.
If the Widget code is called without a settings URL, it SHOULD signal an error.

### Creation from the `widget_collection` endpoint

OPTIONAL, probably deprecated:
The Widget MAY receive as only settings information the Widget creation endpoint (`widget_collection`) with the name of the `@type` of its server-side information..
In that case, it SHOULD present a settings creation interface, where it will POST its settings (with application/x-www-form-urlencoded or multipart/form-data)
The information it POSTs on its creation endpoint MUST contain the `@type` argument it received..
The information POSTed MAY also contain an initial value for `settings` and `user_state` information, as stringified JSON arguments the POSTS. This is a shortcut to PUTting that information separately, and will often save a step.
NOTE: It is not clear that shortcut will be implemented by all backends. The Widget code should check the `widget_info` back for presence of settings, and make a separate PUT call accordingly.
The Widget will obtain its `widget_info` URL back in the HTTP Location header.

## Lifecycle

There are many lifecycle options. 

### Creativity session lifecycle

1. Discussion admin creates a creativity session Widget configuration on an idea.  This includes setting cards, session root idea, etc.
2. User clicks on a URL (inside the session's root idea panel) including the `widget_state`
3. Widget uses `widget_state`, `user_state` and api points.

### Inspire me lifecycle

1. Discussion admin creates a Inspire me Widget configuration, setting cards deck, you tube option, etc.
2. User clicks on a URL (based in any idea panel) including the `widget_state` and idea ID as a GET argument.
3. Widget stores idea ID in `user_state` and proceeds from there.

The widget may also store the user's interaction with that specific idea in the user_state. (For example, remembering which card was used to create which idea.)

### Voting lifecycle

1. Discussion admin creates a voting session configuration. This will include a set of ideas to be voted on, a voting method (ranking, boolean, etc.) and a set of criteria ideas to use. (In the form of an array of array-ID.) 
There will be an API endpoint to get the realized array of all criteria ideas.
(Eventually, we will use idea subtypes, but implementation 0 will probably be for criteria to be the children of a given idea, and likewise for the voting targets.) 

    /data/Conversation/1/widgets/2?target=local:GenericIdeaNode/20
    {
        "criteria": [{"@id":"local:GenericIdeaNode/11", "short_title":"price"}, {"@id":"local:GenericIdeaNode/12", "short_title":"quality"}],
        "criteria_url": "/data/Conversation/1/widgets/criteria",
        "voting_urls": {"local:GenericIdeaNode/11": "/data/Conversation/1/widgets/2/criteria/11/targets/20/votes",
                        "local:GenericIdeaNode/12": "/data/Conversation/1/widgets/2/criteria/12/targets/20/votes"},
        "user_votes_uri": "/data/Conversation/1/widgets/2/targets/20/votes",
        "vote_results_url": "/data/Conversation/1/widgets/2/targets/20/votes/results"}
    }

2. User clicks on a URL (based in any idea panel) including the `widget_state` and voted idea ID as a GET argument.
Widget checks the `user_state` for previous votes on the set of ideas.

## Idea know about their widget relationships

In the case of the creativity session, we have a designated root_idea. We need to go back from the idea to that session.

We also need to go from an idea created within a widget to the Creativity session or InspireMe Widget that proposed it.
In both those cases, we need access to some extra information, such as the inspiring card URI or Youtube URI.

Finally, we need to go from a votable/voted idea to the voting widget, but maybe also to display voting results on the idea after the vote is over.

In all cases, we need access to a typed widget-idea link from the Ideas.
If the frontend (or backend) needs extra Widget-specific information, it should navigate from this link to the Widget representation, which should give all necessary URIs. It may imply that the backend will have to implement specific views that introspect the Widget's JSON.

## Other endpoints

The Widget may have other endpoint URLs than `widget_configuration` and `widget_display`. In particular, it may have endpoints with enough information to restore state. Such endpoints may have shared-knowledge parameters.
[NOT SOLVED, TBD]

## Security considerations

Right now, there is a single endpoint for `user_state`. There is also an endpoint for `user_states`, with all values of all user states.
That endpoint is public, to allow the frontend to compute voting tallies, etc.
We MAY reserve a different endpoint for `private_user_state`.
Another option is to compute aggregate information on the server in appropriate endpoints, but that implies shared knowledge.
