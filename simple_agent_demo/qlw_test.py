# !pip install smolagents[litellm]
from smolagents import CodeAgent, LiteLLMModel
from airsim_smol_wrapper import *
model = LiteLLMModel(
    model_id="volcengine/doubao-1-5-pro-32k-250115", # This model is a bit weak for agentic behaviours though
    api_base="https://ark.cn-beijing.volces.com/api/v3", # replace with 127.0.0.1:11434 or remote open-ai compatible server if necessary
    api_key="cff5bb39-3e44-46da-b5b5-89b963bfd473", # replace with API key if necessary，写自己的key
    flatten_messages_as_text=True, #不写多步骤可能会出错
)


refer_info = """
想象一下您正在帮助我与 AirSim 模拟器进行交互。

我们正在控制一个实体Agent。在任何给定时间点，您都具有以下能力。您还需要输出某些请求的代码。
问题 - 向我提出一个澄清问题
原因 - 解释你为什么这样做。
代码 - 输出达到预期目标的代码命令。

除了工具库外，您还可以使用 Python 库中的函数，例如 math、numpy 等。准备好了吗？
"""

agent = CodeAgent(tools=[takeoff,land], model=model)


agent.run(
    "起飞无人机",
    additional_args={"refer_info":refer_info}
)




agent = CodeAgent(tools=[takeoff,get_drone_position, fly_to, fly_path, set_yaw, get_yaw, get_position, look_at,
                        turn_left, turn_right, forward, detect], model=model)


command = """
无人机目前已经起飞了，现在我需要你帮我找到一个门洞。目标可能散布在场景中，请向右转7次，看看它是否变得可见。请探索并找到门洞。
"""

result1 = agent.run(
    command
    #additional_args={"refer_info":refer_info}
)



obj_id_list, obj_locs,img_with_box = detect_with_img("doorway")

print(img_with_box)


command = """
你已经起飞了，现在需要向前飞5米，进入房间
"""

agent.run(
    command
)

agent = CodeAgent(tools=[takeoff,get_drone_position, fly_to, fly_path, set_yaw, get_yaw, get_position, look_at,
                        turn_left, turn_right, forward, look], model=model
                  )

command = """
好的，现在已经飞进屋子里了，现在能看到屋子里都有啥？
"""

result1 = agent.run(
    command
)