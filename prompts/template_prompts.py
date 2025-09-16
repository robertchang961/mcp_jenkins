"""Template prompts."""

persona = "你是一個擁有十年以上經驗的資深自動化開發工程師及資深 Python 程式設計師。"

prompt_get_job_default_params = """
請使用 MCP 取得 Jenkins Jobs 的預設參數 "{job_name}"。

請將搜尋結果以表格方式回覆。
"""

prompt_get_job_baseurl = """
請使用 MCP 取得 Jenkins Jobs 的基本 URL "{job_name}"。

請將搜尋結果以編號列表方式回覆。
"""

prompt_search_job = """
請使用 MCP 搜尋 Jenkins 所有符合字串 "{search_string}" 的 Jobs。

是否要區分大小寫：{is_case_sensitive}

是否要在特定的 view 下搜尋：{view_name}

請將搜尋結果以編號列表方式回覆。
"""

prompt_clone_job = """請使用 MCP 從 Jenkins Job "{job_name}" 複製一個新的 Job "{new_job_name}"。"""

prompt_rename_job = """請使用 MCP 將 Jenkins Job "{job_name}" 重新命名為 "{new_job_name}"。"""

prompt_delete_job = """請使用 MCP 刪除 Jenkins Job "{job_name}"。"""

prompt_build_job = """
請使用 MCP 建立 Jenkins Job "{job_name}"。

如果該 Job 有參數，請使用以下參數值：
{params}
"""

prompt_get_views = """
請使用 MCP 取得 Jenkins 所有 Views。

請將搜尋結果以編號列表方式回覆。
"""

prompt_get_view_baseurl = """
請使用 MCP 取得 Jenkins View 的基本 URL "{view_name}"。

請將搜尋結果以編號列表方式回覆。
"""

prompt_add_job_to_view = """請使用 MCP 將 Jenkins Job "{job_name}" 加入到 View "{view_name}"。"""

prompt_remove_job_from_view = """請使用 MCP 將 Jenkins Job "{job_name}" 移除出 View "{view_name}"。"""

prompt_stop_last_build = """
請使用 MCP 停止 Jenkins Job "{job_name}" 的最後一個建置。
"""

prompt_get_last_build_info = """
請使用 MCP 取得 Jenkins Job "{job_name}" 的最後一個建置資訊。

請將搜尋結果以表格方式回覆。
"""
