import os
import glob
import yaml

def parse_and_split_list_file(file_path):
    direct_rules = []
    proxy_rules = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # 1. 跳过空行以及以 # 或 // 开头的纯注释行（如 #name）
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # 2. 提取行内注释
            comment = ""
            rule_part = line
            if '#' in line:
                rule_part, comment = line.split('#', 1)
            elif '//' in line:
                rule_part, comment = line.split('//', 1)

            # 3. 清除规则与注释多余空格（彻底删除行内注释）
            rule = rule_part.strip()
            comment = comment.strip()

            if not rule:
                continue

            # 4. 根据行内注释是否包含“直连”分类
            if "直连" in comment:
                direct_rules.append(rule)
            else:
                proxy_rules.append(rule)

    return direct_rules, proxy_rules

def save_list_file(file_path, rules):
    with open(file_path, 'w', encoding='utf-8') as f:
        for rule in rules:
            f.write(f"{rule}\n")

def save_yaml_file(file_path, rules):
    yaml_data = {'payload': rules}
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def main():
    # 设定输出文件夹
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)

    # 优先查找根目录或 rules/ 目录下的 main.list 或任意 .list 文件
    list_files = glob.glob("rules/*.list") + glob.glob("*.list")
    
    # 过滤掉输出目录中的文件，避免重复读取
    list_files = [f for f in list_files if not f.startswith(output_dir)]

    if not list_files:
        print("❌ 未找到任何 .list 源文件！")
        return

    for list_file in list_files:
        filename = os.path.basename(list_file)
        base_name = os.path.splitext(filename)[0]

        direct_rules, proxy_rules = parse_and_split_list_file(list_file)

        # 处理并保存直连规则
        if direct_rules:
            save_list_file(os.path.join(output_dir, f"{base_name}_direct.list"), direct_rules)
            save_yaml_file(os.path.join(output_dir, f"{base_name}_direct.yaml"), direct_rules)
            print(f"✅ 生成直连规则 ({len(direct_rules)} 条): {base_name}_direct.list / .yaml")

        # 处理并保存代理规则
        if proxy_rules:
            save_list_file(os.path.join(output_dir, f"{base_name}_proxy.list"), proxy_rules)
            save_yaml_file(os.path.join(output_dir, f"{base_name}_proxy.yaml"), proxy_rules)
            print(f"✅ 生成代理规则 ({len(proxy_rules)} 条): {base_name}_proxy.list / .yaml")

if __name__ == "__main__":
    main()
