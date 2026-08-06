import os
import yaml

def parse_and_split_list_file(file_path):
    """
    解析源 .list 文件，提取规则本体并按注释分类
    """
    direct_rules = []
    proxy_rules = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # 过滤空行，以及以 # 或 // 开头的纯注释行（如 #name）
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # 提取并分离行内注释
            comment = ""
            rule_part = line
            if '#' in line:
                rule_part, comment = line.split('#', 1)
            elif '//' in line:
                rule_part, comment = line.split('//', 1)

            rule = rule_part.strip()
            comment = comment.strip()

            if not rule:
                continue

            # 判断行内注释是否包含“直连”
            if "直连" in comment:
                direct_rules.append(rule)
            else:
                proxy_rules.append(rule)

    return direct_rules, proxy_rules

def save_list_file(file_path, rules):
    """保存为纯文本 .list 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for rule in rules:
            f.write(f"{rule}\n")

def save_yaml_file(file_path, rules):
    """保存为 YAML 格式文件"""
    yaml_data = {'payload': rules}
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def main():
    # 锁定源文件路径
    target_file = "rules/emby.list"
    output_dir = "generated"

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(target_file):
        print(f"❌ 找不到指定的源文件: {target_file}")
        return

    # 解析 rules/emby.list
    direct_rules, proxy_rules = parse_and_split_list_file(target_file)

    # 1. 导出直连规则 (generated/emby_direct.list 与 generated/emby_direct.yaml)
    if direct_rules:
        save_list_file(os.path.join(output_dir, "emby_direct.list"), direct_rules)
        save_yaml_file(os.path.join(output_dir, "emby_direct.yaml"), direct_rules)
        print(f"✅ 生成直连规则 ({len(direct_rules)} 条): generated/emby_direct.list / .yaml")

    # 2. 导出代理规则 (generated/emby_proxy.list 与 generated/emby_proxy.yaml)
    if proxy_rules:
        save_list_file(os.path.join(output_dir, "emby_proxy.list"), proxy_rules)
        save_yaml_file(os.path.join(output_dir, "emby_proxy.yaml"), proxy_rules)
        print(f"✅ 生成代理规则 ({len(proxy_rules)} 条): generated/emby_proxy.list / .yaml")

if __name__ == "__main__":
    main()
