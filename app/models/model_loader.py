import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
from app.core.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """
        加载本地大模型和分词器
        """
        try:
            logger.info(f"正在加载模型: {settings.MODEL_NAME} 从路径: {settings.MODEL_PATH}")
            logger.info(f"使用设备: {self.device}")
            
            # 加载分词器
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.MODEL_PATH,
                trust_remote_code=True
            )
            
            # 加载模型
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_PATH,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            logger.info("模型加载成功")
            return True
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            return False
    
    def generate_text(self, prompt, max_length=2048, temperature=0.7, top_p=0.9):
        """
        使用模型生成文本
        """
        if not self.model or not self.tokenizer:
            success = self.load_model()
            if not success:
                return {"error": "模型加载失败"}
        
        try:
            # 准备输入
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # 生成文本
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True
                )
            
            # 解码输出
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # 移除原始提示
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):]
                
            return generated_text.strip()
        except Exception as e:
            logger.error(f"文本生成失败: {str(e)}")
            return {"error": f"文本生成失败: {str(e)}"}

# 创建全局模型加载器实例
model_loader = ModelLoader()