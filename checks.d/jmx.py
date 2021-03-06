from checks.jmx_connector import JmxCheck, JMXMetric, convert

class JMXCustomMetric(JMXMetric):


    @property
    def type(self):
        if hasattr(self, '_metric_type'):
            return self._metric_type
        return "gauge"
    
    @property
    def metric_name(self):
        if hasattr(self, '_metric_name'):
            return self._metric_name
        name = ['jmx', self.domain, self.attribute_name]
        return convert(".".join(name))



 
class JMX(JmxCheck):

    def check(self, instance):
        (host, port, user, password, jmx, instance_name) = self._load_config(instance)
        tags = {}
        if instance_name is not None:
            tags['instance'] = instance_name
        dump = jmx.dump()

        self.get_and_send_jvm_metrics(instance, dump, tags)
        self.create_metrics(instance, self.get_beans(dump), JMXCustomMetric, tags=tags)
        self.send_jmx_metrics()
        self.clear_jmx_metrics()


    @staticmethod
    def parse_agent_config(agentConfig):

        return JmxCheck.parse_agent_config(agentConfig, 'java')





