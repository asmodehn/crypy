import asyncio
import prompt_toolkit
from prompt_toolkit.eventloop import use_asyncio_event_loop
from prompt_toolkit.application import Application

# Tell prompt_toolkit to use asyncio for the event loop.
use_asyncio_event_loop()

# Define application.
application = Application(
    layout=None,
    style=None,
    include_default_pygments_style=True,
    style_transformation=None,
    key_bindings=None, clipboard=None,
    full_screen=False, color_depth=None,
    mouse_support=False,

    enable_page_navigation_bindings=None,  # Can be None, True or False.

    paste_mode=False,
    editing_mode=prompt_toolkit.enums.EditingMode.EMACS,
    erase_when_done=False,
    reverse_vi_search_direction=False,
    min_redraw_interval=None,
    max_render_postpone_time=0,

    on_reset=None, on_invalidate=None,
    before_render=None, after_render=None,

    # I/O.
    input=None, output=None
)

# Run the application, and wait for it to finish.
asyncio.get_event_loop().run_until_complete(
    application.run_async().to_asyncio_future())


