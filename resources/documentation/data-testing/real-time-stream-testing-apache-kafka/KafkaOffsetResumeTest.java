import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.KafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

@Testcontainers
class KafkaOffsetResumeTest {

    @Container
    static final KafkaContainer kafka = new KafkaContainer(
        DockerImageName.parse("confluentinc/cp-kafka:7.6.0"));

    @Test
    void consumerResumesFromCommittedOffsetAfterCrash() throws Exception {
        produce(100);

        var consumed = consumeAll("group-1", 100);
        assertThat(consumed).hasSize(100);

        // Same groupId, new consumer = crash/restart simulation.
        // Committed offset means nothing replays.
        var replayed = consumeAll("group-1", 100);
        assertThat(replayed).isEmpty();
    }

    private void produce(int count) throws Exception {
        var props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers());
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        try (var producer = new KafkaProducer<String, String>(props)) {
            for (int i = 0; i < count; i++) {
                producer.send(new ProducerRecord<>("orders", "key-" + i, "order-" + i)).get();
            }
        }
    }

    private List<String> consumeAll(String groupId, int maxPolls) {
        var props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafka.getBootstrapServers());
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        var records = new ArrayList<String>();
        try (var consumer = new KafkaConsumer<String, String>(props)) {
            consumer.subscribe(List.of("orders"));
            for (int i = 0; i < maxPolls && records.size() < 100; i++) {
                var polled = consumer.poll(Duration.ofMillis(500));
                polled.forEach(r -> records.add(r.value()));
            }
            consumer.commitSync();
        }
        return records;
    }
}
