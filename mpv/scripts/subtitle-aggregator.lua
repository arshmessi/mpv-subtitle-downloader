local options = require 'mp.options'
local input = require 'mp.input'
local utils = require 'mp.utils'

local opts = {
    hotkey = 'b',
    selection_hotkey = 'B',
    correction_hotkey = 'C',
    language = 'en',
    profile = 'default',
}
options.read_options(opts, 'subtitle-aggregator')

local selection_bindings = {}

local function clear_selection()
    for _, binding in ipairs(selection_bindings) do
        mp.remove_key_binding(binding)
    end
    selection_bindings = {}
end

local function download_result(result_id)
    clear_selection()
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

mp.add_key_binding(opts.hotkey, 'subtitle-search', function() search(false) end)
mp.add_key_binding(opts.selection_hotkey, 'subtitle-selection', function() search(true) end)
mp.add_key_binding(opts.correction_hotkey, 'subtitle-correct-identity', correct_identity)