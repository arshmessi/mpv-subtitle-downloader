local options = require 'mp.options'

local opts = {
    hotkey = 'b',
    selection_hotkey = 'B',
    language = 'en',
    profile = 'default',
}
options.read_options(opts, 'subtitle-aggregator')

local function search(interactive)
    local path = mp.get_property('path') or ''
    mp.osd_message('Searching subtitles...')
    local command = {'mpv-subtitle', 'search', path, '--language', opts.language}
    if interactive then table.insert(command, '--interactive') end
    mp.commandv('run', unpack(command))
end

mp.add_key_binding(opts.hotkey, 'subtitle-search', function() search(false) end)
mp.add_key_binding(opts.selection_hotkey, 'subtitle-selection', function() search(true) end)