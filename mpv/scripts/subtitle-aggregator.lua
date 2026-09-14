local options = require 'mp.options'
local input = require 'mp.input'
local utils = require 'mp.utils'

local opts = {
    hotkey = 'b',
    language = 'en',
    profile = 'default',
}
options.read_options(opts, 'subtitle-aggregator')

local selection_bindings = {}
local menu_bindings = {}
local menu_index = 1
local menu_open = false

local function clear_selection()
    for _, binding in ipairs(selection_bindings) do
        mp.remove_key_binding(binding)
    end
    selection_bindings = {}
end

local function clear_menu()
    for _, binding in ipairs(menu_bindings) do
        mp.remove_key_binding(binding)
    end
    menu_bindings = {}
    menu_open = false
end

local function download_result(result_id)
    clear_selection()
    clear_menu()
    mp.osd_message('Downloading subtitle ' .. result_id .. '...')
    mp.command_native_async({
        name = 'subprocess',
        args = {'mpv-subtitle', 'download-result', result_id, '--json'},
        capture_stdout = true,
        capture_stderr = true,
    }, function(success, result, error)
        if not success or not result or result.status ~= 0 then
            mp.osd_message('Subtitle download failed: ' .. (error or (result and result.stderr) or 'unknown error'))
            return
        end
        local payload = utils.parse_json(result.stdout or '')
        if not payload or not payload.success or not payload.path then
            mp.osd_message('Subtitle download returned no file')
            return
        end
        mp.commandv('sub-add', payload.path, 'select')
        mp.osd_message('Subtitle loaded')
    end)
end

local function show_results(payload)
    clear_selection()
    if not payload or not payload.results or #payload.results == 0 then
        mp.osd_message(payload and payload.message or 'No suitable subtitles found')
        return
    end
    local lines = {'Subtitle Results — ' .. (payload.media.title or 'current media')}
    for _, report in ipairs(payload.providers or {}) do
        local marker = report.status == 'success' and '[OK]' or '[WARN]'
        lines[#lines + 1] = string.format('%s %s: %s results (%s)', marker, report.provider, report.result_count or 0, report.status or 'unknown')
    end
    for index, item in ipairs(payload.results) do
        local providers = table.concat(item.providers or {item.provider}, ', ')
        lines[#lines + 1] = string.format('%d. %.0f %s %s %s', index, item.score or 0, item.language or '', providers, item.release or '')
        if index >= 9 then break end
    end
    lines[#lines + 1] = 'Press 1-9 to select, Esc to cancel'
    mp.osd_message(table.concat(lines, '\n'), 10)
    for index, item in ipairs(payload.results) do
        if index > 9 then break end
        local key = tostring(index)
        local binding = 'subtitle-select-' .. key
        selection_bindings[#selection_bindings + 1] = binding
        mp.add_forced_key_binding(key, binding, function() download_result(item.result_id) end)
    end
    local cancel_binding = 'subtitle-select-cancel'
    selection_bindings[#selection_bindings + 1] = cancel_binding
    mp.add_forced_key_binding('ESC', cancel_binding, function()
        clear_selection()
        mp.osd_message('Subtitle selection cancelled')
    end)
end

local function run_search(interactive, title, season, episode, imdb_id)
    local path = mp.get_property('path') or ''
    title = title or mp.get_property('media-title') or mp.get_property('filename') or ''
    mp.osd_message('Searching subtitles...')
    local command = {'mpv-subtitle', 'search', path, '--language', opts.language, '--json'}
    if title ~= '' then
        table.insert(command, '--media-title')
        table.insert(command, title)
    end
    if season then table.insert(command, '--season'); table.insert(command, season) end
    if episode then table.insert(command, '--episode'); table.insert(command, episode) end
    if imdb_id then table.insert(command, '--imdb-id'); table.insert(command, imdb_id) end
    mp.command_native_async({
        name = 'subprocess',
        args = command,
        capture_stdout = true,
        capture_stderr = true,
    }, function(success, result, error)
        if not success or not result or result.status ~= 0 then
            mp.osd_message('Subtitle search failed: ' .. (error or (result and result.stderr) or 'unknown error'))
            return
        end
        local payload = utils.parse_json(result.stdout or '')
        if interactive then
            show_results(payload)
        elseif payload and payload.results and payload.results[1] then
            download_result(payload.results[1].result_id)
        else
            mp.osd_message(payload and payload.message or 'No suitable subtitles found')
        end
    end)
end

local function search(interactive)
    run_search(interactive)
end

local function correct_identity()
    local current_title = mp.get_property('media-title') or mp.get_property('filename') or ''
    input.get({
        prompt = 'Subtitle title: ',
        default_text = current_title,
        submit = function(title)
            if title and title ~= '' then
                run_search(true, title)
            else
                mp.osd_message('Identity correction cancelled')
            end
        end,
    })
end

local menu_items = {
    {label = 'Quick search and load best match', action = function() run_search(false) end},
    {label = 'Search and choose a subtitle', action = function() run_search(true) end},
    {label = 'Correct media title and search', action = correct_identity},
}

local function render_menu()
    local lines = {'Subtitle Aggregator'}
    for index, item in ipairs(menu_items) do
        local marker = index == menu_index and '> ' or '  '
        lines[#lines + 1] = marker .. item.label
    end
    lines[#lines + 1] = 'Up/Down to navigate, Enter to select, Esc to cancel'
    mp.osd_message(table.concat(lines, '\n'), 30)
end

local function open_menu()
    if menu_open then return end
    clear_selection()
    menu_open = true
    menu_index = 1
    render_menu()
    for _, key in ipairs({'UP', 'DOWN', 'ENTER', 'ESC'}) do
        menu_bindings[#menu_bindings + 1] = 'subtitle-menu-' .. key
    end
    mp.add_forced_key_binding('UP', menu_bindings[1], function()
        menu_index = (menu_index - 2) % #menu_items + 1
        render_menu()
    end)
    mp.add_forced_key_binding('DOWN', menu_bindings[2], function()
        menu_index = menu_index % #menu_items + 1
        render_menu()
    end)
    mp.add_forced_key_binding('ENTER', menu_bindings[3], function()
        local action = menu_items[menu_index].action
        clear_menu()
        action()
    end)
    mp.add_forced_key_binding('ESC', menu_bindings[4], function()
        clear_menu()
        mp.osd_message('Subtitle menu cancelled')
    end)
end

mp.add_key_binding(opts.hotkey, 'subtitle-menu', open_menu)